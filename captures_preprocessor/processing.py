#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "February 2020"

from glob import glob
from read_json import ReadJson
from database import DataFile
from database import Queries
from utilities import LoggingClass
from database import MySQLDatabase
from datetime import datetime, timedelta

rj = ReadJson()
log = LoggingClass('',True).get_logger()

class CaptureFoldersList(object):
    def __init__(self, cameras_path):
        self.cameras_path = cameras_path

    def create_list(self):
        cameras_path_list = glob(self.cameras_path + '/*/')
        return cameras_path_list

class MonthsString(object):
    def __init__(self, months_number):
        self.months_number = int(months_number) 

    def create_strings(self):
        all_months = [(datetime.now() + timedelta(-30*(i))).strftime('%Y%m') for i in range(self.months_number)]
        return all_months

class DoWork(object):
    def __init__(self, filename):
        self.filename = filename
        self.dbuser = rj.get_db_user()
        self.dbpwd = rj.get_db_pwd()
        self.dbname = rj.get_db_name()
        self.dbhost = rj.get_db_host()
        self.dbport = rj.get_db_port()

        self.db = MySQLDatabase(self.dbuser, self.dbpwd, self.dbname, self.dbhost, self.dbport)
        self.Session = self.db.mysql_session()

    def do_work(self):
        t1 = datetime.now()
        try:
            rows = Queries(self.Session, DataFile, self.filename).match_filename()
            if not rows:
                return self.filename
        except Exception as e:
            msg = "Query on database excep - DoWork.do_work --"
            log.error("{0}{1}".format(msg,e))
        return rows
