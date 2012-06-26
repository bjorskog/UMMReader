#!/usr/bin/env python

"""
Testing all settings in the config-file vs
hardcoded values.
"""

import logging
from nose.tools import assert_equal, assert_not_equal
from ummreader.config import UmmConfig

logger = logging.getLogger('umm-parser')
config = UmmConfig()

def test_username():
    """ Testing username """
    pass

def test_password():
    """ Testing password """
    pass

def test_path():
    """ Testing path """
    assert_equal(config.path, 'UMM')

def test_ftphost():
    """ Testing FTP hostname """
    assert_equal(config.ftphost, 'ftp.nordpoolspot.com')

def test_last():
    """ Testing the last value """
    last = config.last 
    assert_equal(last, 53795)
    assert_not_equal(config.last, 53796)

def test_tempdir():
    """ Testing the tempdir """
    assert_equal(config.tempdir, '/tmp/ummxmls')
