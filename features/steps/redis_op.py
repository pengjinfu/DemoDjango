# -*- coding: utf-8 -*-
# coding=utf-8
'''
@author: Wilson
'''

import redis

def getKeyV(key):
    #node =redis.StrictRedis(host='fb-redis.darlp4.ng.0001.apse1.cache.amazonaws.com',port=6379)
    node =redis.StrictRedis(host='127.0.0.1',port=6379)
    return node.get(key)

def getHMap(key):
    #node =redis.StrictRedis(host='fb-redis.darlp4.ng.0001.apse1.cache.amazonaws.com',port=6379)
    node =redis.StrictRedis(host='127.0.0.1',port=6379)
    return node.hgetall(key)

def setHMap(name,key,value):
    #node =redis.StrictRedis(host='fb-redis.darlp4.ng.0001.apse1.cache.amazonaws.com',port=6379)
    node =redis.StrictRedis(host='127.0.0.1',port=6379)
    return node.hset(name,key,value)

def delKey(key):
    #node =redis.StrictRedis(host='fb-redis.darlp4.ng.0001.apse1.cache.amazonaws.com',port=6379)
    node =redis.StrictRedis(host='127.0.0.1',port=6379)
    return node.delete(key)

def getKeys():
    #node =redis.StrictRedis(host='fb-redis.darlp4.ng.0001.apse1.cache.amazonaws.com',port=6379)
    node =redis.StrictRedis(host='127.0.0.1',port=6379)
    return node.keys()