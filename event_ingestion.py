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
from glob import glob
from read_tools import read_json
from mysql_tools import mysql_session
from mysql_tools import select_event
from folder_size import folder_size 
from table_objects import data_file
from read_tools import read_txt
from shutil import Error

#
CWD = os.getcwd()
logfile = open(CWD + '/' + "logfile.txt",'a')
cnf = read_json('conf.json',CWD,logfile) 
#
event_path = cnf['eventpath']
os.chdir(event_path)
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
    if not event_archived and event_list[j][0:4]=='2020':
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
foreign_stations_list = read_txt(stations_file,CWD,logfile) 
events_to_process_path_list = glob(dest_folder + '/*')
for i in events_to_process_path_list:
    station_folders_path_list = glob(i + '/*/')
    station_fullnames_list = [os.path.basename(os.path.normpath(j)) for j in station_folders_path_list]
    station_names_list = [i[:-19] for i in station_fullnames_list]
    for j in range(len(station_names_list)):
	if station_names_list[j] not in foreign_stations_list:
	    thumbnail_path = glob(station_folders_path_list[j]+"/*-thumb.jpg")
	    try:
		shutil.copy(thumbnail_path[0],os.path.join(thumb_dest_folder,station_fullnames_list[j] + '.jpg'))
	    except IOError as err:
		logfile.write('%s -- IO.Error: %s \n' % (datetime.now(),err))
#
logfile.close()
