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

rj = ReadJson()
rsync_path = rj.get_rsync_path()
prep_path = rj.get_preproc_path()

class FolderSize(object):
    '''Result in Unix block size'''
    def __init__(self, path):
        self.path = path

    def get_folder_size(self):
        total_size = 0
        if not isdir(self.path):
            return 0
        for dirpath,dirnames,filenames in os.walk(self.path):
            for f in filenames:
                fp = os.path.join(dirpath,f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
        return total_size

class ReadStations(object):
    def __init__(self, filename):
        self.filename = filename

    def _get_stations_list(self):
        filepath = '%s/%s' % (os.getcwd(), self.filename)
        stations_list = []
        with open(filepath, 'r') as filehandle:
            for line in filehandle:
                currentPlace = line[:-1]
                stations_list.append(currentPlace)
        return stations_list

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
        self.fail_path = rj.get_failures_path()
        self.thumb_path = rj.get_thumbs_path()
        self.event_folder = os.path.join(prep_path, self.event_str) 

    def get_stations_names(self):
        station_path = glob(self.event_folder + '/*/')
        station_fullname = [os.path.basename(os.path.normpath(k)) for k in station_path]
        station_name = [k[:-19] for k in station_fullnames]
        return station_path, station_fullname, station_name

    def run(self):
        self.recipient = rj.get_recipient()
        self.sender = rj.get_sender()
        self.smtphost = rj.get_smtp_host()
        sp, sf, sn = self.get_station_names()

        for j in range(len(sn)):
	    fits_path = glob(sp[j] + "/*.fit")
            event_str_full = self.event_str + '_UT'
            failure_folder = os.path.join(self.fail_path, sf[j])
            station_original_path = os.path.join(self.rsync_path, event_full_name, sf[j])
            size_origin = FolderSize(station_original_path).get_folder_size() 
            size_dest = FolderSize(sp[j]).get_folder_size()

            if size_origin != size_dest:
                msg = "Event alert: folder size mismatch after copy. Event affected: " + self.event_str
                SendEmail(msg, self.recipient, self.sender, self.smtphost).send_email()
                shutil.move(self.event_folder, self.failure_folder)
            else:
                if fits_path and not os.stat(fits_path[0]).st_size == 0:
                    thumbfile_path = glob(sp[j] + "/*-thumb.jpg")
                    if thumbfile_path:
                        shutil.copy(thumbfile_path[0],os.path.join(self.thumb_path, sf[j] + '.jpg'))
