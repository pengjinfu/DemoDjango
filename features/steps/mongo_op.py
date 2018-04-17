# -*- coding: utf-8 -*-
# coding=utf-8
'''
@author: Wilson
'''
from bson.objectid import ObjectId
from pymongo import *
from features.steps.config import *

def getMongoClient(env):
    mongoConfig = mongo_test
    if env == "TEST":
        mongoConfig = mongo_test
    if env == "PRE":
        mongoConfig = mongo_online
    if env == "ONLINE":
        mongoConfig = mongo_online
    return MongoClient(mongoConfig["host"], mongoConfig["port"])


# 查询数据库
# env：运行环境信息，用于获取数据库连接信息
# db_name: 数据库名称
# collention: 表名
# limit: 返回的最大行数
def mongo_select(env,db_name,collection,sqlJson,limit=None):
    mclient = getMongoClient(env)
    db = mclient[db_name]
    collection_useraction = db[collection]
    if limit is None:
        return (collection_useraction.find(sqlJson),collection_useraction.find(sqlJson).count())
    else:
        return (collection_useraction.find(sqlJson).limit(limit),collection_useraction.find(sqlJson).count())
    #return db.collection_useraction.count()

# 插入数据库
# env：运行环境信息，用于获取数据库连接信息
# db_name: 数据库名称
# collention: 表名
def mongo_insert(env,db_name,collection,sqlJson):
    mclient = getMongoClient(env)
    db = mclient[db_name]
    collection_useraction = db[collection]
    #return collection_useraction.insert(sqlJson).inserted_id
    return collection_useraction.insert(sqlJson)

#{"classifyid":"test1"}, {"$set":{"keyword.0.name":'test5'}}
def mongo_update(env,db_name,collection,criteria,objNew):
    mclient = getMongoClient(env)
    db = mclient[db_name]
    collection_useraction = db[collection]
    collection_useraction.update(criteria,objNew)

def mongo_delete(env,db_name,collection,sqlJson):
    mclient = getMongoClient(env)
    db = mclient[db_name]
    collection_useraction = db[collection]
    collection_useraction.remove(sqlJson)

#select
# sql = {"nick":"shangfei1984"}
# results = mongo_select("FlyNews","user",sql)
# print(results[0])
# userId = results[0]["_id"]
# print(userId)

#insert
userFeeds = {
  "language": "555066f4113f4a2f158b4567",
  "userId": "573586255cbb3d345d8b460a",
  "userType": 2,
  "feedIds": {
    "56cabb3d26e7b5c8cd17d03d": "另一半到底是玩咖還是認真？　5個特點看清男人的「定性」",
    "56cabb3d26e7b5c8cd17d010": "孔敏智公開親筆信 稱在2NE1的時光十分幸福",
    "56cabb3d26e7b5c8cd17d02a": "SBL／劉錚西進 下周赴大陸談合約",
    "56cabb3d26e7b5c8cd17d01f": "[NBA] PG：為隊友驕傲 夏天會幫溜馬招募",
    "56cabb3d26e7b5c8cd17d011": "",
    "56f64bfe913207633b8b4567 ": "",
    "56cabb3d26e7b5c8cd17d039": "輔英校花 顏子寧",
    "56cabb3d26e7b5c8cd17cfd4": "你最想被哪個韓國男藝人求婚？狙擊大韓民國所有女心的前四名",
    "56d017f791320717328b4570": ""
  }
}
# insert_ID = mongo_insert("FlyNews","userFeeds",sql)
# print(insert_ID)
#
# #update
# sql = {"userId":userId}
# results = mongo_select("FlyNews","userFeeds",sql)
# for u in results:
#     print(u)
# #results["feedIds"]["56f64bfe913207633b8b1111"] = "asdusahduashdusahudhasd"
# sql1 = {"_id":insert_ID}
# sql2 = {"$set":{"userType": 5}}
# mongo_update("FlyNews","userFeeds",sql1,sql2)
