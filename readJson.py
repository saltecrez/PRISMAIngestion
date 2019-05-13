#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "June 2018"

import json

def readJson(filename,CWD):
    JSON_CONFIG_FILE_PATH='%s/%s' % (CWD, 'config.json')
    CONFIG_PROPERTIES={}
    try:
        with open(JSON_CONFIG_FILE_PATH) as data_file:
            CONFIG_PROPERTIES=json.load(data_file)
        return CONFIG_PROPERTIES
    except IOError as e:
            print e
            print 'IOError: Unable to open config.json. Terminating execution.'
            exit(1)
