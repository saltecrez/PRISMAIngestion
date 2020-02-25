#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "February 2020"

import os
from glob import glob
from read_json import ReadJson
from database import MySQLDatabase 
from queries import Queries
from mapping import DataFile

rj = ReadJson()

class CheckEventString(object):
    def __init__(self):
        self.events_folder = rj.get_event_folder()

    def _check_event_string(self):
        event_paths = glob(self.events_folder + '/*')
        event_strings = [os.path.basename(i)[0:15] for i in event_paths]
        output_list = []
        for i in event_strings:
            if i[0].isdigit() and i[8] == 'T':
                output_list.append(i)
            else:
                pass
        return output_list

class SelectEventString(object):
    def __init__(self):
        self.dbhost = rj.get_db_host()
        self.dbuser = rj.get_db_user()
        self.dbpwd = rj.get_db_pwd()
        self.dbname = rj.get_db_name()

        self.db = MySQLDatabase(self.dbuser, self.dbpwd, self.dbhost, self.dbname)
        self.Session = self.db.create_session()

    def _filter_event(self, event_string):
        valid_session = self.db.validate_session()
        if valid_session:
            rows = Queries(self.Session, DataFile, event_string).match_event()
            if not rows:
                return event_string
   
    def get_selected_events_list(self): 
        checked_list = CheckEventString()._check_event_string() 
        selected_list = []
        for i in checked_list:
            if self._filter_event(i) is not None:
                selected_list.append(self._filter_event(i))
        return selected_list
