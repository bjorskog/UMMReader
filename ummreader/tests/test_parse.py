#!/usr/bin/env python

"""
Unittests for all parsing.
"""

import pprint
from ummreader.parser import xml2dict

LOCALPATH = '/Users/bjorskog/envs/umm.reader/UMMReader/ummreader/data/'

def test_xml2dict():
    """ Testing to parse an XML-message """
    file = LOCALPATH + '53791.xml'
    umm = xml2dict(file)
    print '\n'
    pprint.pprint(umm)

def test_many_xml2dict():
    """ Testing to parse many XML messages """
    files = ('53791.xml', '53796.xml', '53927.xml')
    for item in files:
        print "\n"
        print "Parsing a UMM."
        print "=========================="
        file = LOCALPATH + item
        umm = xml2dict(file)
        pprint.pprint(umm)
