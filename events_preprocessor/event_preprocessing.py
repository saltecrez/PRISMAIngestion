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

rj = ReadJson()
rsync_path = rj.get_rsync_path()
prep_path = rj.get_preproc_path()

class CopyToPreprocessingArea(object):
    def __init__(self, event_str):
        self.event_str = event_str
        self.st_file = rj.get_foreign_stations_filename()

    def copy_folder(self):
        ignore_lst = [i + '*' for i in ReadStations(self.st_file)._get_stations_list()]
        event_str_full = self.event_str + '_UT'
        source = os.path.join(rsync_path, event_str_full)
        dest = os.path.join(prep_path, self.event_str)
        shutil.copytree(source, dest, symlinks=True, ignore=ignore_patterns(*ignore_lst))        

class EventPreprocessing(object):
    def __init__(self, event_str):
        self.event_str = event_str
        self.event_folder = os.path.join(prep_path, self.event_str) 

    def get_stations_names(self):
        station_path = glob(self.event_folder + '/*/')
        station_fullname = [os.path.basename(os.path.normpath(k)) for k in station_path]
        station_name = [k[:-19] for k in station_fullname]
        return station_path, station_fullname, station_name

    def run(self):
        self.fail_path = rj.get_failures_path()
        self.thumb_path = rj.get_thumbs_path()
        self.ingest_path = rj.get_ingestion_path()
        self.recipient = rj.get_recipient()
        self.sender = rj.get_sender()
        self.smtphost = rj.get_smtp_host()
        sp, sf, sn = self.get_stations_names()

        for j in range(len(sn)):
            fitsfile_path = glob(sp[j] + '/*.fit')
            event_str_full = self.event_str + '_UT'
            failure_folder = os.path.join(self.fail_path, sf[j])
            station_original_path = os.path.join(rsync_path, event_str_full, sf[j])
            size_origin = FolderSize(station_original_path).get_folder_size() 
            size_dest = FolderSize(sp[j]).get_folder_size()

            if size_origin != size_dest:
                msg = 'Event alert: folder size mismatch after copy. Event: ' + self.event_str
                SendEmail(msg, self.recipient, self.sender, self.smtphost).send_email()
                shutil.move(self.event_folder, self.failure_folder)
            else:
                if fitsfile_path and not os.stat(fitsfile_path[0]).st_size == 0:
                    thumbfile_path = glob(sp[j] + '/*-thumb.jpg')
                    if thumbfile_path:
                        shutil.copy(thumbfile_path[0],os.path.join(self.thumb_path, sf[j] + '.jpg'))

                    fitsname = os.path.basename(fitsfile_path[0])
                    fits_path_renamed = os.path.join(sp[j], 'Sum_' + fitsname)
                    os.rename(fitsfile_path[0],fits_path_renamed)
                    FitsAddKey(fits_path_renamed, 'EVENT', self.event_str, 'Event label').fits_add_key()

                    folder_elements = sum([len(files) for r, d, files in os.walk(sp[j])])                    
                    os.chdir(self.event_folder)
                    tar = TarHandling(sf[j])
                    exit_bool = tar.create_tarfile()
                    if exit_bool == True:
                        tar_elements = int(tar.count_tar_elements())
                        if tar_elements == folder_elements:
                            shutil.copy(sf[j] + '.tar.gz', self.ingest_path)
                        else:
                            msg = 'Frames number in tar and in original folder do not match. Event ' + self.event_str + ' - moved to FAILURES folder'
                            SendEmail(msg, self.recipient, self.sender, self.smtphost).send_email()
                            shutil.move(sf[j] + '.tar.gz', self.fail_path + sf[j] + '.tar.gz')
                            
    def remove_event(self):
        shutil.rmtree(self.event_folder)
