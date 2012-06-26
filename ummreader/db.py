#!/usr/bin/env python

""" 
Utils for writing UMMs to the database, and to
get information back from it.
"""

import logging
from pymongo import Connection, DESCENDING, ASCENDING
from pymongo.errors import ConnectionFailure

from ummreader.config import UmmConfig

logger = logging.getLogger('umm-parser')
config = UmmConfig()

__all__ = ['get_last', 'insert_one', 'get_one', 'get_many',\
               'drop_collection', 'get_first']

def get_last(everything=False):
    """ Getting the last UMM (id only) """
    logger.info('Getting last UMM from MongoDB.')
    try:
        conn = Connection(config.host, config.port)
        database = conn[config.database]
        collection = database[config.collection]
        res = collection.find().sort('umm_number', DESCENDING)
        if res.count() == 0:
            return None
        elif res.count() > 0 and everything:
            return res[0]
        elif res.count() > 0 and not everything:
            return res[0]['umm_number']
    except ConnectionFailure, exception:
        logger.error('Error connecting to the database: %s' % exception)

def get_first(everything=True):
    """ Getting the first UMM (id only) """
    logger.info('Getting first UMM from MongoDB.')
    try:
        conn = Connection(config.host, config.port)
        database = conn[config.database]
        collection = database[config.collection]
        res = collection.find().sort('umm_number', ASCENDING)
        if res.count() == 0:
            return None
        elif res.count() > 0 and everything:
            return res[0]
        elif res.count() > 0 and not everything:
            return res[0]['umm_number']
    except ConnectionFailure, exception:
        logger.error('Error connecting to the database: %s' % exception)
    
def insert_one(umm):
    """ Inserting one UMM to the db """
    logger.info('Inserting umm %s.' % umm['umm_number'])
    try:
        conn = Connection(config.host, config.port)
    except ConnectionFailure, exception:
        logger.error('Error connecting to the database: %s' % exception)
    database = conn[config.database]
    collection = database[config.collection]
    res = collection.find_one({'umm_number':umm['umm_number']})
    if res is None:
        collection.insert(umm)
    else:
        collection.update(res, umm, upsert=True)
    
def get_one(key, value):
    """ Retrieving one UMM based on key, value """
    logger.info('Retrieving %s from database.' % key)
    try:
        conn = Connection(config.host, config.port)
    except ConnectionFailure, exception:
        logger.error('Error connecting to the database: %s' % exception)
    database = conn[config.database]
    collection = database[config.collection]
    res = collection.find_one({key:value})
    return res

def get_many(key, value):
    """ Get many UMMs based on key, value """
    logger.info('Retrieving %s from database.' % key)
    try:
        conn = Connection(config.host, config.port)
    except ConnectionFailure, exception:
        logger.error('Error connecting to the database: %s' % exception)
    database = conn[config.database]
    collection = database[config.collection]
    res = collection.find({key:value})
    return 

def drop_collection():
    """ Drops the collection """
    logger.info('Dropping the connection %s on %s.'\
                    % (config.collection, config.database))
    try:
        conn = Connection(config.host, config.port)
    except ConnectionFailure, exception:
        logger.error('Error dropping collection: %s' % exception)
    database = conn[config.database]
    collection = database[config.collection]
    collection.drop()

