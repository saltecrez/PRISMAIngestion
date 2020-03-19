#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "February 2020"

import os
import shutil
from glob import glob
from os.path import isdir
from database import Queries
from database import DataFile
from read_json import ReadJson
from utilities import SendEmail
from utilities import FitsAddKey
from utilities import TarHandling 
from utilities import ReadStations 
from utilities import FolderSize
from utilities import LoggingClass
from database import MySQLDatabase
from shutil import ignore_patterns

log = LoggingClass('',True).get_logger()
rj = ReadJson()
rsync_path = rj.get_rsync_path()

class SelectEventString(object):
    def __init__(self):
        self.dbhost = rj.get_db_host()
        self.dbuser = rj.get_db_user()
        self.dbpwd = rj.get_db_pwd()
        self.dbport = rj.get_db_port()
        self.dbname = rj.get_db_name()

        self.db = MySQLDatabase(self.dbuser, self.dbpwd, self.dbname, self.dbhost, self.dbport)
        self.Session = self.db.mysql_session()

    def _check_event_string(self):
        '''Check the event string matches roughly YYYYMMDDTHHMMSS format'''
        try:
            event_folders = glob(rsync_path + '/*')
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

    def _filter_event(self, event_string):
        '''Check if an event string is found in database'''
        try:
            rows = Queries(self.Session, DataFile, event_string).match_event()
            if not rows:
                return event_string
        except Exception as e:
            msg = "Query on database excep - SelectEventString._filter_event --"
            log.error("{0}{1}".format(msg,e))

    def get_selected_events_list(self):
        '''Create list of event strings with YYYYMMDDTHHMMSS format and not found in database'''
        try:
            checked_list = self._check_event_string()
            selected_list = []
            for i in checked_list:
                if self._filter_event(i) is not None:
                    selected_list.append(self._filter_event(i))
            return selected_list
        except Exception as e:
            msg = "Creation of events already in db excep - SelectEventString.get_selected_events_list --"
            log.error("{0}{1}".format(msg,e))

class EventPreprocessing(object):
    def __init__(self, event_str):
        rj = ReadJson()
        self.event_str = event_str
        self.prep_path = rj.get_preproc_path()
        self.fail_path = rj.get_failures_path()
        self.thumb_path = rj.get_thumbs_path()
        self.ingest_path = rj.get_ingestion_path()
        self.recipient = rj.get_recipient()
        self.sender = rj.get_sender()
        self.smtphost = rj.get_smtp_host()
        self.st_file = rj.get_foreign_stations_filename()
        self.event_folder = os.path.join(self.prep_path, self.event_str) 
        self.event_str_full = self.event_str + '_UT'

    def copy_to_preprocessing_area(self):
        '''Copy event folder to preprocessing area. Leave out foreign folders'''
        ignore_lst = [i + '*' for i in ReadStations(self.st_file)._get_stations_list()]
        event_str_full = self.event_str + '_UT'
        source = os.path.join(rsync_path, event_str_full)
        dest = os.path.join(self.prep_path, self.event_str)
        if not os.path.exists(dest):
            try:
                shutil.copytree(source, dest, symlinks=True, ignore=ignore_patterns(*ignore_lst))
            except Exception as e:
                msg = "Copy event folder excep -- EventPreprocessing.copy_to_preprocessing_area --"
                log.error("{0}{1}".format(msg,e))
        else:
            pass

    def _get_stations_names(self):
        try:
            station_path = glob(self.event_folder + '/*/')
            station_fullname = [os.path.basename(os.path.normpath(k)) for k in station_path]
            station_name = [k[:-19] for k in station_fullname]
            return station_path, station_fullname, station_name
        except Exception as e:
            msg = "Copy event folder excep -- EventPreprocessing._get_stations_names --"
            log.error("{0}{1}".format(msg,e))

    def _compare_sizes(self, stat_fullname, station_path):
        '''Stations folder size comparison between rsync and preprocessing areas'''
        station_original_path = os.path.join(rsync_path, self.event_str_full, stat_fullname)
        size_origin = FolderSize(station_original_path).get_folder_size()
        size_dest = FolderSize(station_path).get_folder_size()
        if size_origin != size_dest:
            msg = 'Event alert: folder size mismatch after copy. Event: ' + self.event_str
            SendEmail(msg, self.recipient, self.sender, self.smtphost).send_email()
            try:
                shutil.move(self.event_folder, self.failure_folder)
                return False
            except Exception as e:
                msg = "Move event folder excep -- EventPreprocessing._compare_sizes --"
                log.error("{0}{1}".format(msg,e))
        else:
            return True

    def _fits_manipulation(self, fitspath, station_path):
        '''Rename summary FITS file and add EVENT key'''
        try:
            fitsname = os.path.basename(fitspath)
            fits_path_renamed = os.path.join(station_path, 'Sum_' + fitsname) 
            os.rename(fitspath,fits_path_renamed)
            FitsAddKey(fits_path_renamed, 'EVENT', self.event_str, 'Event label').fits_add_key()
        except Exception as e:
            msg = "FITS manipulation excep -- EventPreprocessing._fits_manipulation --"
            log.error("{0}{1}".format(msg,e))

    def process_event(self):
        sp, sf, sn = self._get_stations_names()

        for j in range(len(sn)):
            fitsfile_path = glob(sp[j] + '/*.fit')
            failure_folder = os.path.join(self.fail_path, sf[j])

            if self._compare_sizes(sf[j], sp[j]):
                if fitsfile_path and not os.stat(fitsfile_path[0]).st_size == 0:

                    thumbfile_path = glob(sp[j] + '/*-thumb.jpg')
                    if thumbfile_path:
                        try:
                            shutil.copy(thumbfile_path[0],os.path.join(self.thumb_path, sf[j] + '.jpg'))
                        except Exception as e:
                            msg = "Copy thumb file excep -- EventPreprocessing.process_event --"
                            log.error("{0}{1}".format(msg,e))

                    self._fits_manipulation(fitsfile_path[0], sp[j])

                    folder_elements = sum([len(files) for r, d, files in os.walk(sp[j])])                    

                    os.chdir(self.event_folder)
                    tar = TarHandling(sf[j])

                    exit_bool = tar.create_tarfile()
                    if exit_bool == True:
                        tar_elements = int(tar.count_tar_elements())
                        if tar_elements == folder_elements:
                            try:
                                shutil.copy(sf[j] + '.tar.gz', self.ingest_path)
                            except Exception as e:
                                msg = "Copy .tar.gz to ingestion folder excep -- EventPreprocessing.process_event --"
                                log.error("{0}{1}".format(msg,e))
                        else:
                            msg = ('Frames nr in tar and in original folder do not match. Event ' +  
                                    self.event_str + ' - moved to FAILURES folder')
                            SendEmail(msg, self.recipient, self.sender, self.smtphost).send_email()
                            try:
                                shutil.move(sf[j] + '.tar.gz', self.fail_path + sf[j] + '.tar.gz')
                            except Exception as e:
                                msg = "Move tar.gz to failures folder excep -- EventPreprocessing.process_event --"
                                log.error("{0}{1}".format(msg,e))
                            
    def remove_event(self):
        try:
            shutil.rmtree(self.event_folder)
        except Exception as e:
            msg = "File removal exception --"
            log.error("{0}{1}".format(msg,e)) 
