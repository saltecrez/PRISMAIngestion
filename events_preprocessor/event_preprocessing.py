#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "February 2020"

import os
import shutil
from glob import glob
from os.path import isdir
from read_json import ReadJson
from shutil import ignore_patterns
from utilities import SendEmail
from utilities import FitsAddKey
from utilities import TarHandling 
from utilities import ReadStations 
from utilities import FolderSize
from utilities import LoggingClass

log = LoggingClass('',True).get_logger()

class EventPreprocessing(object):
    def __init__(self, event_str):
        rj = ReadJson()
        self.event_str = event_str
        self.rsync_path = rj.get_rsync_path()
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
        source = os.path.join(self.rsync_path, event_str_full)
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
        station_original_path = os.path.join(self.rsync_path, self.event_str_full, stat_fullname)
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
