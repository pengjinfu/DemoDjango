import json

import sys


class FileClass:
    def __init__(self, name):
        self.name = name

    def read_file(self, file_path):
        f = open(file_path, 'r')

        x = json.dumps([1, 'a', 'b'])
        json.dump(x, f)

    def file_to_arr(self, filepath):
        data = []
        try:
            with open(filepath) as f:
                for line in f:
                    data.append(line)
        except OSError as err:
            print("OS error: {0}".format(err))
        except ValueError:
            print("Could not convert data to an integer.")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        return data

    def to_string(self):
        return 'file class name ' + self.name


class ExtendClass(FileClass):

    def get_file_info(self, file_path):
        return self.read_file(file_path)

    def generator(self, data):
            for index in range(len(data) - 1, -1, -1):
                yield data[index]
