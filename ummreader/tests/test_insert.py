#!/usr/bin/env python

"""
Unittests for all communication with MongoDB.
"""

import pprint
from ummreader.parser import xml2dict
from ummreader.db import insert_one, get_one, get_last

LOCALPATH  =  '/Users/bjorskog/envs/umm.reader/UMMReader/ummreader/data'

def test_insert():
    """ Testing to insert a UMM to the db """
    file = LOCALPATH + '/53791.xml'
    umm = xml2dict(file)
    insert_one(umm)

def test_get():
    """ Testing to get one UMM from the db """
    print "\nGrabbing UMM from database."
    umm = get_one('umm_number', 53791)
    pprint.pprint(umm)

def test_get_last():
    """ Testing to get the last inserted UMM """
    print '\nGetting the last UMM.'
    item = get_last()
    print item
