#!/usr/bin/env python

'''scribe_tail: A simple script for sending messages to scribe.'''

import os, sys, time
import re
import argparse
from scribe import scribe
from thrift.transport import TTransport, TSocket
from thrift.protocol import TBinaryProtocol
import socket
import logging
import logging.handlers
import traceback


class Tailer(object):
    """\
    Implements tailing functionality like GNU tail commands.

    Based on: http://pypi.python.org/pypi/tailer
    """
    line_terminators = ('\r\n', '\n', '\r')

    def __init__(self, file):
        self.file = file
        self.start_pos = self.file.tell()

    def seek(self, pos, whence=0):
        self.file.seek(pos, whence)

    def time_is_up_to_flush(self, last, now, flush_interval):
        return (now - last > flush_interval)

    def follow(self, delay=1.0, flush_interval=3.0, start=None):
        """\
        Iterator generator that returns lines as data is added to the file.

        Based on: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/157035
        """
        trailing = True
        last_flush_time = time.time()

        if start == None:
            with_start = False
        else:
            with_start = True

        while 1:

            if with_start:
                whence = start
                with_start = False
            else:
                whence = self.file.tell()

            self.seek(whence)

            line = self.file.readline()
            if line:
                if trailing and line in self.line_terminators:
                    # This is just the line terminator added to the end of the
                    # file before a new line, ignore.
                    trailing = False
                    continue

                if line[-1] in self.line_terminators:
                    line = line[:-1]
                    if line[-1:] == '\r\n' and '\r\n' in self.line_terminators:
                        # found crlf
                        line = line[:-1]

                trailing = False
                next_whence = self.file.tell()
                # flush, line, whence
                yield False, line, next_whence
            else:
                trailing = True
                self.seek(whence)

                if self.time_is_up_to_flush(last_flush_time, time.time(),
                                            flush_interval):
                    last_flush_time = time.time()
                    # flush, line, whence
                    yield True, None, None

                time.sleep(delay)

    def __iter__(self):
        return self.follow()

    def close(self):
        self.file.close()


class Scribe(object):
    def __init__(self, host="127.0.0.1", port=1463, category=None):
        self.category = category
        self.host = host
        self.port = port
        self.socket = TSocket.TSocket(host=self.host, port=self.port)
        self.transport = TTransport.TFramedTransport(self.socket)
        self.protocol = TBinaryProtocol.TBinaryProtocol(trans=self.transport,
                                                        strictRead=False, strictWrite=False)
        self.client = scribe.Client(iprot=self.protocol, oprot=self.protocol)
        self.transport.open()

    def send(self, msg):
        log_entry = scribe.LogEntry(category=self.category, message=msg)
        return self.client.Log(messages=[log_entry])

    def close(self):
        self.transport.close()

    def __del__(self):
        self.close()

    def send(self, msg):
        log_entry = scribe.log(category=self.category, message=msg)
        return self.client.Log(messages=[log_entry])

    def close(self):
        self.transport.close()

    def __del__(self):
        self.close()


class FailStore(object):
    def __init__(self, target_file=None, path=None, when='h', interval=1,
                 backup_count=5):
        fail_store_filename = 'scribe_tail_fail_store.log'
        fail_store_full_path = None
        if path:
            fail_store_full_path = os.path.join(path, fail_store_filename)
        else:
            dir_of_target_file = os.path.dirname(
                os.path.abspath(target_file.name))
            fail_store_full_path = os.path.join(dir_of_target_file,
                                                fail_store_filename)

        self.logger = logging.getLogger('SribeTailFailStore')
        self.logger.setLevel(logging.ERROR)

        formatter = logging.Formatter('%(message)s')
        handler = logging.handlers.TimedRotatingFileHandler(
            fail_store_full_path, when=when, interval=interval,
            backupCount=backup_count)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log(self, msg):
        self.logger.error(msg)


class WhenceStore(object):
    def __init__(self, target_file, rewind=False):
        self.whence_file_name = target_file.name + '.scribe_tail_whence'
        if not self.exists():
            self.touch()
        self.f = open(self.whence_file_name, 'r+')
        if rewind:
            self.whence(0)

    def touch(self):
        open(self.whence_file_name, 'w').close()

    def exists(self):
        return os.path.exists(self.whence_file_name)

    def whence_file_ready(self):
        return (self.f and not self.f.closed)

    def start(self):
        if self.whence_file_ready():
            self.f.seek(0)
            start = self.f.read().strip()
            if start == "":
                return None
            else:
                return int(start)
        else:
            return None

    def whence(self, whence):
        assert type(whence) in (int, long), 'whence must be int or long'
        if self.whence_file_ready():
            self.f.seek(0)
            self.f.write(str(whence))
            self.f.truncate()
            self.f.flush()

    def __del__(self):
        self.f.close()


def follow(scribe_client, target_file, delay=1.0, flush_interval=10.0,
           read_line_buf_size=100, whence_store=None, fail_store=None):
    read_line_buf = []

    tailer = Tailer(target_file)

    for time_to_flush, line, whence in tailer.follow(delay, flush_interval,
                                                     whence_store.start()):

        if time_to_flush:
            if len(read_line_buf) != 0:
                flush(read_line_buf, scribe_client,
                      whence_store=whence_store,
                      fail_store=fail_store)
        else:
            read_line_buf.append((line, whence))
            if len(read_line_buf) >= read_line_buf_size:
                flush(read_line_buf, scribe_client,
                      whence_store=whence_store,
                      fail_store=fail_store)


def flush(lines, scribe_client, whence_store=None, fail_store=None):
    whence_store.whence(lines[-1][1])

    data = '\n'.join([lw[0] for lw in lines]) + '\n'

    result = None

    try:

        result = scribe_client.send(data)

    except TTransport.TTransportException as e:
        fail_store.log(data)
        traceback.print_exc(file=sys.stdout)
    except socket.error as e:
        fail_store.log(data)
        traceback.print_exc(file=sys.stdout)

    if result == scribe.ResultCode.OK:
        pass
    elif result == scribe.ResultCode.TRY_LATER:
        fail_store.log(data)
        print
        'Scribe error: TRY_LATER'
    else:
        fail_store.log(data)
        print
        'Scribe error: Unknown'

    del lines[:]


def parse_args():
    parser = argparse.ArgumentParser(prog='scribe_tail',
                                     description='Follow file and send data to scribe.')
    parser.add_argument('FILE', metavar='FILE', type=open, nargs=1,
                        help='target file name')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 0.3')
    parser.add_argument('-c', '--category', required=True,
                        help='scribe category')
    parser.add_argument('-l', '--host', default='127.0.0.1',
                        help='scribe host (default: 127.0.0.1)')
    parser.add_argument('-p', '--port', default=1463, type=int,
                        help='scribe port (default: 1463)')
    parser.add_argument('--rewind', type=bool, default=False,
                        help='start read the file from the beginning (default: false)')
    parser.add_argument('--follow_delay', type=float, default=0.5,
                        help='follow file delay(Sec) (default: 0.5)')
    parser.add_argument('--read_line_buf_size', type=int, default=100,
                        help='read line buffer size (default: 100)')
    parser.add_argument('--flush_interval', type=float, default=10.0,
                        help='flush read line buffer interval(Sec) (default: 10.0)')
    parser.add_argument('--fail_store_path',
                        help='store path to write scribe send failed data '
                             '(default: same with FILE\'s directory)')
    parser.add_argument('--fail_store_log_rotate_when',
                        choices=['S', 'M', 'H', 'D', 'W', 'midnight'], default='H',
                        help='fail store log rotate when '
                             'depending on the rollover interval (default: H). '
                             'for more information, visit http://docs.python.org/library/logging.handlers.html#timedrotatingfilehandler')
    parser.add_argument('--fail_store_log_rotate_rollover_interval', type=int,
                        default=1, help='fail store log rotate rollover interval'
                                        '(default: 1)')
    parser.add_argument('--fail_store_backup_count', type=int, default=5,
                        help='fail store file backup count (default: 5)')
    return parser.parse_args()


def main():
    args = parse_args()
    target_file = args.FILE[0]

    # Scribe client
    scribe_client = Scribe(host=args.host, port=args.port,
                           category=args.category)
    # Whence to start
    whence_store = WhenceStore(target_file, rewind=args.rewind)

    # Fail store
    fail_store = FailStore(target_file=target_file,
                           path=args.fail_store_path,
                           when=args.fail_store_log_rotate_when,
                           interval=args.fail_store_log_rotate_rollover_interval,
                           backup_count=args.fail_store_backup_count)

    # Follow the file and send data to scribe
    follow(scribe_client, target_file,
           delay=args.follow_delay,
           flush_interval=args.flush_interval,
           read_line_buf_size=args.read_line_buf_size,
           whence_store=whence_store,
           fail_store=fail_store)


if __name__ == "__main__":
    # print("aaa")
     main()
