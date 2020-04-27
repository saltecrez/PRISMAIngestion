#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "February 2020"

import os
from glob import glob
import multiprocessing
from database import Queries
from database import DataFile
from read_json import ReadJson
from multiprocessing import Pool
from utilities import LoggingClass
from database import MySQLDatabase
from datetime import datetime 
from datetime import timedelta

log = LoggingClass('',True).get_logger()
rj  = ReadJson()

dbuser = rj.get_db_user()
dbpwd  = rj.get_db_pwd()
dbname = rj.get_db_name()
dbhost = rj.get_db_host()
dbport = rj.get_db_port()

db      = MySQLDatabase(dbuser, dbpwd, dbname, dbhost, dbport)
Session = db.mysql_session()

def _query_filename(filename):
    try:
        rows = Queries(Session, DataFile, filename).match_filename()
        if not rows:
            return filename
    except Exception as e:
        msg = "Query on database excep - _query_filename --"
        log.error("{0}{1}".format(msg,e)) 

class CamerasPathList(object):
    def __init__(self, cameras_path):
        self.cameras_path = cameras_path

    def create_list(self):
        cameras_path_list = glob(self.cameras_path + '/*/')
        return cameras_path_list

class MonthsString(object):
    def __init__(self, months_number):
        self.months_number = months_number 

    def create_strings(self):
        all_months = [(datetime.now() + timedelta(-30*(i))).strftime('%Y%m') for i in range(self.months_number)]
        return all_months

class ArchiveFITS(object):
    def __init__(self, camera, month):
        self.camera = camera
        self.month = month
        self.ingest_path = rj.get_ingestion_path()
        self.thumbs_path = rj.get_thumbs_path()
        self.threads_nr  = rj.get_threads_number() 
        self.cameras_month_path = self.camera + self.month
    
    def _create_fitslist(self):
        self.fitslist = glob(self.cameras_month_path + '/*.fit')
        return self.fitslist

    def _multithreaded_select(self):
        selects = [os.path.basename(i) + '.gz' for i in self._create_fitslist()]
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        pool = multiprocessing.Pool(processes=self.threads_nr)
        not_found_in_db = pool.map_async(_query_filename, selects).get()
        return not_found_in_db

    def copy_fits(self):
        not_found_in_db = self._multithreaded_select()
        for i in not_found_in_db:
            if i is not None:
                name = os.path.splitext(os.path.normpath(i))[0]
                if not os.path.exists(os.path.join(self.ingest_path,name)):
                    path = self.cameras_month_path + '/' + name
                    try:
#                        #shutil.copy(path,os.path.join(self.ingest_path,name))
                        print(name)
                    except shutil.Error as e:
                        msg = "Copy FITS excep -- ArchiveFITS.copy_fits --"
                        log.error("{0}{1}".format(msg,e))

    def copy_jpg(self):
        for i in self._create_fitslist():
            base_string = os.path.basename(os.path.splitext(os.path.normpath(i))[0])
            jpg500_name = base_string + '-500x500.jpg'
            jpg_name = base_string + '.jpg'
            jpg_destination = os.path.join(self.thumbs_path,jpg_name)
            jpg_original_path = os.path.join(self.cameras_month_path,jpg500_name)
            if not os.path.exists(jpg_destination) and os.path.exists(jpg_original_path):
                try:
                     #shutil.copy(jpg_original_path,jpg_destination)
                    print(jpg_original_path)
                    print(jpg_destination)
                except shutil.Error as e:
                    msg = "Copy jpg thumbnail excep -- ArchiveFITS.copy_jpg --"
                    log.error("{0}{1}".format(msg,e))
