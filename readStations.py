#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "June 2018"


def readStations(filename,CWD):
    filepath='%s/%s' % (CWD, filename)
    mylist = []
    try:
        with open(filepath, 'r') as filehandle:
            for line in filehandle:
               # remove linebreak which is the last character of the string
               currentPlace = line[:-1]
               mylist.append(currentPlace)
        return mylist
    except IOError as e:
        print e
        print 'IOError: Unable to open stations list file. Terminating execution.'
        exit(1)

