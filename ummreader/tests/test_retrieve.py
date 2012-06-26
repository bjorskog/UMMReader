#!/usr/bin/env python

"""
Testing all functions to get stuff from the FTP server.
"""

import pprint
import logging

from ummreader.core import config
from ummreader.utils import get_file, get_contents, get_filelist

logger = logging.getLogger('umm-parser')

def test_retrieve():
    """ Testing to get a file from FTP """
    filename = '53791.xml'
    get_file(filename,
             config.path,
             config.ftphost,
             config.username,
             config.password)

def test_contents():
    """ Testing to get folder contents from FTP """
    files = get_contents(config.path,
                         config.ftphost, 
                         config.username,
                         config.password)
    last = 53795
    print '\nWe start with file %i.xml.' % last
    print '\nSo we start with %i files.' % len(files)
    print 'Now removing files later than %i.' % last
    files.sort()
    pprint.pprint(files)
    def func(item):
        itemnumber = int(item.split('.')[0])
        if itemnumber <= last:
            return False
        else:
            return True
    files = filter(func, files) 
    print '\nAnd we are left with %i.' % len(files)
    pprint.pprint(files)

def test_get_filelist():
    """ Testing to get a list of files """
    files = ('54364.xml', '54365.xml')
    get_filelist(files, config.path, config.ftphost,
                 config.username, config.password)
