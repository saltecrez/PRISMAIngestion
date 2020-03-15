#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "February 2020"

import os
from glob import glob
from read_json import ReadJson
from database import MySQLDatabase 
from database import Queries
from database import DataFile

rj = ReadJson()

class CheckEventString(object):
    def __init__(self):
        self.rsync_path = rj.get_rsync_path()

    def _check_event_string(self):
        try:
            event_folders = glob(self.rsync_path + '/*')
            event_strings = [os.path.basename(i)[0:15] for i in event_folders]
            output_list = []
            for i in event_strings:
                if i[0].isdigit() and i[8] == 'T':
                    output_list.append(i)
                else:
                    pass
            return output_list
        except Exception as e:
            msg = "String event selection excep - CheckEventString._check_event_string --"
            log.error("{0}{1}".format(msg,e))  	

class SelectEventString(object):
    def __init__(self):
        self.dbhost = rj.get_db_host()
        self.dbuser = rj.get_db_user()
        self.dbpwd = rj.get_db_pwd()
        self.dbport = rj.get_db_port()
        self.dbname = rj.get_db_name()

        self.db = MySQLDatabase(self.dbuser, self.dbpwd, self.dbname, self.dbhost, self.dbport)
        self.Session = self.db.mysql_session()

    def _filter_event(self, event_string):
        try:
            rows = Queries(self.Session, DataFile, event_string).match_event()
            if not rows:
                return event_string
        except Exception as e:
            msg = "Query on database excep - SelectEventString._filter_event --"
            log.error("{0}{1}".format(msg,e))
   
    def get_selected_events_list(self): 
        try:
            checked_list = CheckEventString()._check_event_string() 
            selected_list = []
            for i in checked_list:
                if self._filter_event(i) is not None:
                    selected_list.append(self._filter_event(i))
            return selected_list
        except Exception as e:
            msg = "Creation of events already in db excep - SelectEventString.get_selected_events_list --"
            log.error("{0}{1}".format(msg,e))
