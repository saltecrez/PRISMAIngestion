#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "June 2018"

'''
   This tool is supposed to be used for the daily 
   ingestion of event files (PRISMA project)
'''

import os
import shutil
import pymysql
import subprocess
from glob import glob
from read_tools import read_json
from mysql_tools import mysql_session
from mysql_tools import select_event
from folder_size import folder_size 
from table_objects import data_file
from read_tools import read_txt
from create_tarfile import create_tarfile
from shutil import Error
from fits_handling import fits_add_key
from count_tar_elements import count_tar_elements

#
CWD = os.getcwd()
logfile = open(CWD + '/' + "logfile.txt",'a')
cnf = read_json('conf.json',CWD,logfile) 
#
event_path = cnf['eventpath']
event_path_list = glob(event_path + '/*')
event_list = [os.path.basename(i)[0:15] for i in event_path_list]
#
db_host = cnf['dbhost']; db_pwd = cnf['dbpwd']
db_user = cnf['dbuser']; db_name = cnf['dbname']
Session = mysql_session(db_user,db_pwd,db_host,db_name,logfile)
session = Session()
#
dest_folder = cnf['destfolder']
for j in range(len(event_list)):
    event_archived = select_event(session,data_file,event_list[j],logfile)
    if not event_archived and event_list[j][0:4] == '2020':
	size_at_origin = folder_size(event_path_list[j])
	destination = os.path.join(dest_folder,event_list[j])
	try:
	    shutil.copytree(event_path_list[j],destination,symlinks = True)
	except shutil.Error as err:
	    logfile.write('%s -- shutil.Error: %s \n' % (datetime.now(),err))
	size_at_destination = folder_size(destination)
	if size_at_origin != size_at_destination:
	    msg = "Event alert: folder copied in " + dest_folder + "not consistent with folder in " + event_path + "for event " + event_list[j]
	    send_email(msg,recipient,sender,smtp_host,logfile)
	    break
#
stations_file = cnf['stations']
thumb_dest_folder = cnf['thumbpath']
ingestion_folder = cnf['ingfolder']
foreign_stations_list = read_txt(stations_file,CWD,logfile) 
events_to_process_path_list = glob(dest_folder + '/*')
for i in events_to_process_path_list:
    os.chdir(i)
    station_folders_path_list = glob(i + '/*/')
    station_fullnames_list = [os.path.basename(os.path.normpath(k)) for k in station_folders_path_list]
    station_names_list = [k[:-19] for k in station_fullnames_list]
    for j in range(len(station_names_list)):
	if station_names_list[j] not in foreign_stations_list:
	    thumbnail_path = glob(station_folders_path_list[j] + "/*-thumb.jpg")
	    try:
		shutil.copy(thumbnail_path[0],os.path.join(thumb_dest_folder,station_fullnames_list[j] + '.jpg'))
	    except IOError as err:
		logfile.write('%s -- IO.Error: %s \n' % (datetime.now(),err))
#
            fits_path = glob(station_folders_path_list[j] + "/*.fit")
	    if fits_path:
		fits_filename = os.path.basename(fits_path[0])
		fits_path_renamed = station_folders_path_list[j] + 'Sum_' + fits_filename 
		event_string = os.path.basename(os.path.normpath(i))
		os.rename(fits_path[0],fits_path_renamed)
		fits_add_key(fits_path_renamed,'EVENT',event_string,'Event label',logfile)
		tar_filename = station_fullnames_list[j] 
		folder_elements = sum([len(files) for r, d, files in os.walk(station_fullnames_list[j])])
		create_tarfile(tar_filename,tar_filename,logfile)
		tar_elements = int(count_tar_elements(tar_filename,logfile))
		if tar_elements == folder_elements:
		    try:
		        shutil.copy(tar_filename+'.tar.gz',ingestion_folder)	
		    except IOError as err:
			logfile.write('%s -- IO.Error: %s \n' % (datetime.now(),err))
#
logfile.close()
