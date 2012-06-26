#!/usr/bin/env python

""" 
Management of config-stuff for the UMM Reader

"""

from ConfigParser import RawConfigParser
from os.path import dirname, join
import logging

DEFAULT_CONFIG_FILE = 'ummreader.cfg'
DEFAULT_CONFIG_PATH = dirname(__file__)
CONFIG = join(DEFAULT_CONFIG_PATH, DEFAULT_CONFIG_FILE)

DEFAULT_LOG = 'ummreader.log'
LOG = join(DEFAULT_CONFIG_PATH, DEFAULT_LOG)

LOGGER = logging.getLogger('umm-parser')
LOGGER.setLevel(logging.DEBUG)
FILEHANDLER = logging.FileHandler(LOG)
FILEHANDLER.setLevel(logging.DEBUG)
FORMATTER = \
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
FILEHANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(FILEHANDLER)

class UmmConfig(object):
    """ Config for the UMM-reader """
    def __init__(self):
        self._config = RawConfigParser()
        self._config.read(CONFIG)
        
    def _get_field(self, section, field):
        """ Generic method to read values from the config-file """
        if not self._config.has_option(section, field):
            return None
        return self._config.get(section, field).strip()
    
    def _set_field(self, section, field, value):
        """ Generic method to set values to config-file """
        self._config.set(section, field, value)
        with open(CONFIG, 'wb') as configfile:
            try:
                self._config.write(configfile)
            except Exception, exception:
                LOGGER.error('Could not write to file: %s' % exception)
                configfile.close()
        
    @property
    def username(self):
        """ Getter for username """
        return self._get_field('Nordpool', 'username')
    
    @property
    def password(self):
        """ Getter for password """
        return self._get_field('Nordpool', 'password')
    
    @property
    def path(self):
        """ Getter for path """
        return self._get_field('Nordpool', 'path')

    @property
    def ftphost(self):
        """ Getter for FTP-hostname """
        return self._get_field('Nordpool', 'host')
    
    def _get_last(self):
        """ Getter for the last value """
        if not self._config.has_option('UMM', 'last'):
            return None
        return self._config.getint('UMM', 'last')

    def _set_last(self, number):
        """ Setter for the last value """
        self._set_field('UMM', 'last', number)
    last = property(_get_last, _set_last)

    @property
    def host(self):
        """ Getter for the MongoDB host """
        return self._get_field('MongoDB', 'host')

    @property
    def port(self):
        """ Getter for the MongoDB port """
        if not self._config.has_option('MongoDB', 'port'):
            return None
        return self._config.getint('MongoDB', 'port')

    @property
    def database(self):
        """ Getter for the MongoDB database name """
        return self._get_field('MongoDB', 'database')
    
    @property
    def collection(self):
        """ Getter for the MongoDB collection name """
        return self._get_field('MongoDB', 'collection')

    @property
    def tempdir(self):
        """ Getter for the temporary storage """
        return self._get_field('Local', 'tempdir')
