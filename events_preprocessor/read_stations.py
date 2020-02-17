#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "June 2018"

import os

class ReadStations(object):
    def __init__(self, filename):
        self.filename = filename

    def create_stations_list(self):
        filepath = '%s/%s' % (os.getcwd(), self.filename)
        stations_list = []
        with open(filepath, 'r') as filehandle:
            for line in filehandle:
                currentPlace = line[:-1]
                stations_list.append(currentPlace)
        return stations_list

if __name__ == "__main__":
    filename = 'foreign_stations.txt'
    print(ReadStations(filename).create_stations_list())
