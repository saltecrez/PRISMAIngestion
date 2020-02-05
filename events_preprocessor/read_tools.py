#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "June 2018"


import json
import csv
from datetime import datetime


def read_json(filename,cwd,logfile):
    json_config_file_path = '%s/%s' % (cwd,filename)
    config_properties = {}
    try:
        with open(json_config_file_path) as data_file:
            config_properties = json.load(data_file)
    except IOError as e:
        logfile.write('%s -- IOError: %s \n' % (datetime.now(),e))
    else:
	return config_properties


def read_csv(filename,logfile):
    rowlist = []
    try:
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=',')
            for row in csv_reader:
                rowlist.append(row)
    except IOError as e:
        logfile.write('%s -- IOError: %s \n' % (datetime.now(),e))
    else:
	return rowlist


def read_txt(filename,cwd,logfile):
    filepath = '%s/%s' % (cwd,filename)
    mylist = []
    try:
        with open(filepath,'r') as filehandle:
            for line in filehandle:
               currentPlace = line[:-1]
               mylist.append(currentPlace)
    except IOError as e:
	logfile.write('%s -- IOError: %s \n' % (datetime.now(),e))
    else:
	return mylist
