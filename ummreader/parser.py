#!/usr/bin/env python

""" 
Methods for parsing the UMMs and turning them into a dict """

import logging
import datetime
from xml.etree import ElementTree

logger = logging.getLogger('umm-parser')

__all__ = ['xml2dict']

def get_date(string):
    """ Trying to parse the text date into a datetime """
    if string is None:
        return None
    date = None
    datestring = string[:8]
    hourstring = string[-5:]
    hourstring.replace('.',':')
    try:
        datetimestring = datestring + ' ' + hourstring
        date = datetime.datetime.strptime(datetimestring, '%d.%m.%y %H:%M')
    except ValueError, exception:
        logger.error('ValueError parsing the datetime: %s' % exception)
        logger.error('Value: %s' % datetimestring)
    except Exception, exception:
        logger.error('Error parsing the datetime: %s' % exception)
    return date

def xml2dict(sourcefile):
    """ Parsing a XML-message and returning as dict """
    res = {}
    with open(sourcefile, 'rt') as xmlfile:
        tree = ElementTree.parse(xmlfile)
    for node in tree.iter():
        res[node.tag] = node.text
    node = tree.find('umm')
    res['umm_number'] = int(node.attrib['u_id'])
    if node.attrib['new_followup'] == 'Followup':
        res['parent_umm'] = int(node.attrib['parent_id'])
        res['predecessor_umm'] = int(node.attrib['predecessor_id'])
    xmlfile.close()
    if 'participant_umm' in res.keys():
        del res['participant_umm']
        res['umm_type'] = 'participant'
    elif 'tso_umm' in res.keys():
        res['umm_type'] = 'tso'
        del res['tso_umm']
    del res['umm']
    # cleaning up all end-of line chars
    for key, value in res.items():
        try:
            res[key] = value.strip()
        except:
            pass
    # parsing string to dates
    res['approved'] = get_date(res['approved'])
    res['decission'] = get_date(res['decission'])
    res['event_start'] = get_date(res['event_start'])
    res['event_stop'] = get_date(res['event_stop'])
    res['registered'] = get_date(res['registered'])
    return res
