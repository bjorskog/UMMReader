#!/usr/bin/env python

""" 
Utils for managing the FTP source 
"""

from os import chdir, mkdir
from os.path import exists
from ftplib import FTP
from ummreader.config import LOGGER as logger
from ummreader.config import UmmConfig

config = UmmConfig()

__all__ = ['get_file', 'get_filelist', 'get_contents']

def get_file(filename, path, host, username, password, localpath=''):
    """ Will retrieve a specified file from a specific path on a given host, 
    and store it a the local path. """
    try:
        logger.info('Connecting to ftp://%s:%s@%s' % (username, password, host))
        ftp = FTP(host, username, password)
    except Exception, exception:
        logger.error('Error connecting to %s: %s' % (host, exception))
    logger.info('Changing path to %s on FTP server' % path)
    ftp.cwd(path)
    if exists(localpath): 
        chdir(localpath)
    else:
        if not exists(config.tempdir):
            mkdir(config.tempdir)
        chdir(config.tempdir)
    logger.info('Retriving and storing %s.' % filename)
    with open(filename, 'w') as outfile:
        ftp.retrbinary('RETR %s' % filename, outfile.write)
    ftp.quit()
    outfile.close()

def get_filelist(files, path, host, username, password, localpath=''):
    """ Will retrieve a list of files from a specific path on a given host,
    and store it locally at some (optional) path """
    try:
        logger.info('Connecting to ftp://%s:%s@%s' % (username, password, host))
        ftp = FTP(host, username, password)
    except Exception, exception:
        logger.error('Error connecting to %s: %s' % (host, exception))
    logger.info('Changing path to %s on FTP server' % path)
    ftp.cwd(path)
    if exists(localpath):
        chdir(localpath)
    else:
        if not exists(config.tempdir):
            mkdir(config.tempdir)
        chdir(config.tempdir)
    for filename in files:
        with open(filename, 'w') as outfile:
            ftp.retrbinary('RETR %s' % filename, outfile.write)
        outfile.close()
    ftp.quit()

def get_contents(path, host, username, password):
    """ Will return a list of the contents in a given path on a FTP-server. """
    try:
        logger.info('Connecting to ftp://%s:%s@%s' % (username, password, host))
        ftp = FTP(host, username, password)
    except Exception, exception:
        logger.error('Error connecting to %s: %s' % (host, exception))
    logger.info('Changing path to %s on FTP server.' % path)
    ftp.cwd(path)
    files = []
    try:
        files = ftp.nlst()
    except Exception, exception:
        logger.error('Error retrieving file list: %s' % exception)
    for item in files:
        if not 'xml' in item:
            files.remove(item)
    return files

