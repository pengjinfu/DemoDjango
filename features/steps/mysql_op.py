# -*- coding: utf-8 -*-
# coding=utf-8
'''
@author: Wilson
'''
import MySQLdb
from features.steps.config import *


def run_sql(sql, query_num_flag=False,db_info_name=uat_db):
    conn = MySQLdb.connect(host=cfg_mysql['host'], port=cfg_mysql['port'], user=cfg_mysql['user'], passwd=cfg_mysql['passwd'], db=cfg_mysql['db'], charset=cfg_mysql['charset'])
    cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    sql_num = cur.execute(sql)
    result = None

    if not query_num_flag:
        result = cur.fetchall()
        # if result:
        #     result = sorted(list(result))
            # result = sorted(list(result), key=lambda item: item["id"])

    conn.commit()
    cur.close()
    conn.close()

    if query_num_flag:
        return sql_num
    return result, sql_num

def select(sql, query_num_flag=False,db_info_name=uat_db):
    conn = MySQLdb.connect(host='fb-test-dbsql.cpgqn7tqklnb.ap-southeast-1.rds.amazonaws.com',port=3306, user='ad',passwd='425@5g',db='ad',charset='utf8')
    cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    sql_num = cur.execute(sql)
    result = None

    if not query_num_flag:
        result = cur.fetchone()
        # if result:
        #     result = sorted(list(result))
            # result = sorted(list(result), key=lambda item: item["id"])

    conn.commit()
    cur.close()
    conn.close()

    if query_num_flag:
        return sql_num
    return result

def build_insert_sql(table_object):
    insert_template = "insert into %s (%s) values(%s)"


    table_name, obj_attr_dict = retrieve_info(table_object)

    key_str = "`" + "`, `".join(obj_attr_dict.keys()) + "`"
    value_str = "'" + "', '".join(obj_attr_dict.values()) + "'"

    # print("insert sql: " + insert_template % (table_name, key_str, value_str))
    return insert_template % (table_name, key_str, value_str)


def build_delete_sql(table_object):
    table_name, obj_attr_dict = retrieve_info(table_object)

    if table_name is "mob_camp_material":
        delete_template = "delete from %s where mat_id = '%s'"
        # print("delete sql111: " + delete_template % (table_name, obj_attr_dict['mat_id']))
        return delete_template % (table_name, obj_attr_dict['mat_id'])
    else:
        delete_template = "delete from %s where id = '%s'"
        # print("delete sql: " + delete_template % (table_name, obj_attr_dict['id']))
        return delete_template % (table_name, obj_attr_dict['id'])


def retrieve_info(table_object):
    obj_attr_dict = dict(table_object.__dict__)

    table_key = 'table'
    table_name = obj_attr_dict[table_key]
    del obj_attr_dict[table_key]

    return table_name, obj_attr_dict


def delete_history_records(table, field, value):
    sql = "delete from " + table + " where " + field + " like '%" + value + "%'"
    run_sql(sql)


class orm_helper:
    def __init__(self):
        self.table = 'dump'

    def insert_test_record(self):
        self.delete_test_record()
        return run_sql(build_insert_sql(self))
    def delete_test_record(self):
        return run_sql(build_delete_sql(self))


def build_sql_condition(sql_params, logicCondition):
    condition_list = []
    for key, value in sql_params.iteritems():
        if isinstance(value, list) and len(value) > 0:
            condition_list.append(" %s in ('%s') " % (key, "','".join(value)))
        else:
            condition_list.append(" %s = '%s' " % (key, value))

    if len(condition_list) > 0:
        return " where " + str(logicCondition).join(condition_list)
    else:
        return ""