#!/usr/bin/env python

""" 
A simple application to read, parse and insert UMMs.
Main access point for the application.

"""

from os import chdir, listdir, remove
from optparse import OptionParser
from ummreader.utils import *
from ummreader.parser import *
from ummreader.db import *
from ummreader.config import LOGGER as logger
from ummreader.config import UmmConfig

config = UmmConfig()

def first():
    """ Displays the first UMM that exists in the database. """
    logger.info('Presenting the first UMM in the database.')
    umm = get_first()
    if umm is not None:
        messageid = umm['umm_number']
        registered = umm['registered']
        print 'First UMM with id %i was registered %s.' % \
            (messageid, registered)
    else:
        print 'Empty database - no UMM stored.'

def last():
    """ Displays the last UMM that exists in the database. """
    logger.info('Presenting information on last update.')
    umm = get_last(True)
    if umm is not None:
        messageid = umm['umm_number']
        registered = umm['registered']
        print 'Last UMM with id %i was registered %s.' % \
            (messageid, str(registered))
    else:
        print 'Empty database - no UMMs stored.'

def clean():
    """ Erasing all temporary files """
    logger.info('Cleaning the temporary directory.')
    chdir(config.tempdir)
    try:
        for item in listdir(config.tempdir):
            remove(item)
    except OSError, exception:
        logger.error('Could not delete files: %s' % exception)

def update():
    """ Doing the actual updating """
    logger.info('Updating the db...')
    last = get_last()
    logger.info('Starting at %s' % str(last))
    filelist = get_contents(config.path, config.ftphost,
                            config.username, config.password)
    filelist.sort()
    
    def func(item):
        itemnumber = int(item.split('.')[0])
        if itemnumber <= last:
            return False
        else:
            return True

    filelist = filter(func, filelist)

    if len(filelist) > 0:
        logger.info('Will update %i items.' % len(filelist))
        get_filelist(filelist, config.path, config.ftphost,
                     config.username, config.password)
        logger.info('Done retrieving files. Now inserting to db.')
        chdir(config.tempdir)
        for item in listdir(config.tempdir):
            insert(item)
    else:
        logger.info('Nothing to update. Done.')

def insert(filename): 
    """ Adding one file to the db """
    logger.info('Adding %s.' % filename)
    umm = xml2dict(filename)
    insert_one(umm)

def insert_path(path):
    """ Adding all files in the folder """
    logger.info('Adding everything in %s.' % path)
    chdir(path)
    try:
        for item in listdir(path):
            insert(item)
    except OSError, exception:
        logger.error('Could not read files in path: %s' % exception)
    
def drop():
    """ Dropping the collection on the MongoDB """
    drop_collection()

def main():
    """ The main access point. Called from the command line. """
    usage = 'usage: %prog [options] arg'
    description = 'A program to manage UMMs from Nordpool spot FTP-server.'
    optparser = OptionParser(usage=usage, description=description)
    optparser.add_option('-f', '--file-', action='store', 
                         type='string', dest='filename',
                         help='Specify which file to add.')
    optparser.add_option('-s', '--start', action='store_true',
                         dest='start', help='Shows the first UMM in the db.')
    optparser.add_option('-u', '--update', action='store_true',
                         dest='update', help='Updates the db.')
    optparser.add_option('-c', '--clean', action='store_true',
                         dest='clean', help='Deletes all temporary files.')
    optparser.add_option('-p', '--path', action='store',
                         type='string', dest='path', 
                         help='Specify which path to add files from.')
    optparser.add_option('-l', '--last', action='store_true',
                         dest='last', help='Shows the last UMM in the db.')
    optparser.add_option('-d', '--drop', action='store_true',
                         dest='drop', help='Drops the collection in the db.')

    (options, args) = optparser.parse_args()
    
    if options.clean:
        print 'Cleaning the temporary directory...'
        clean()
    if options.filename:
        print 'Inserting %s into the database...' % options.filename
        insert(options.filename)
    if options.update:
        print 'Updating from Nordpools FTP server...'
        update()
    if options.clean and options.update:
        clean()
        update()
    if options.path:
        print 'Inserting all files in %s...' % options.path
        insert_path(options.path)
    if options.last:
        last()
    if options.start:
        first()
    if options.drop:
        answer = raw_input('Dropping the collection...You sure? (Y/N) ')
        if answer.upper() == 'Y':
            print 'Now droppping the collection...'
            drop_collection()
        elif answer.upper() == 'N':
            print 'Skipping.'
