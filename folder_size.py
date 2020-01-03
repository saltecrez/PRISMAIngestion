#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "June 2018"


import os
from os.path import isfile
from os.path import isdir
from datetime import datetime


def folder_size(path):
    total_size = 0
    if not isdir(path):
        return 0
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if isfile(fp):
                    total_size += os.path.getsize(fp)
        return total_size
    except OSError as e:
        logfile.write('%s -- OS.Error: %s \n' % (datetime.now(),e))
