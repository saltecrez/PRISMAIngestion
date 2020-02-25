#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "February 2020"

import os
import shutil
from read_json import ReadJson
from shutil import ignore_patterns
from read_stations import ReadStations

rj = ReadJson()

class CopyToPreprocessingArea(object):
    def __init__(self, event_string):
        self.event_string = event_string
        self.proc_path = rj.get_preprocess_folder()
        self.event_folder = rj.get_event_folder()
        self.stations_file = rj.get_foreign_stations()

    def copy_folder(self):
        ignore_list = [i + '*' for i in ReadStations(self.stations_file).create_stations_list()]
        event_string_full = self.event_string + '_UT'
        destination = os.path.join(self.proc_path, event_string_full)
        source = os.path.join(self.event_folder, event_string_full)
        shutil.copytree(source, destination, symlinks=True, ignore=ignore_patterns(*ignore_list))        
