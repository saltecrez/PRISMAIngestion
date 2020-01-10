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
import read_tools
import mysql_tools
from glob import glob
from shutil import Error
from folder_size import folder_size 
from send_email import send_email
from table_objects import data_file
from create_tarfile import create_tarfile
from fits_handling import fits_add_key
from count_tar_elements import count_tar_elements
from event_string_reader import event_string_reader


CWD = os.getcwd()
logfile = open(CWD + '/' + "logfile.txt",'a')

# Read from configuration file
cnf = read_tools.read_json('conf.json',CWD,logfile) 
event_path    = cnf['eventfolder'];   ingest_path    = cnf['ingestfolder']
proc_path     = cnf['processfolder']; thumbs_path    = cnf['thumbsfolder']
db_host       = cnf['dbhost'];        db_pwd         = cnf['dbpwd']
db_user       = cnf['dbuser'];        db_name        = cnf['dbname']
stations_file = cnf['stations'];      temp_path      = cnf['failurefolder']
smtp_host     = cnf['smtphost'];      sender         = cnf['sender']
recipient     = cnf['email']; 

# create events list from events available in the 
# folder synchronized with the French server 
event_path_list = glob(event_path + '/*')
event_list = [os.path.basename(i)[0:15] for i in event_path_list]
selected_event_list = event_string_reader(event_list)

# create mysql database session
Session = mysql_tools.mysql_session(db_user,db_pwd,db_host,db_name,logfile)
session = Session()
valid_session = mysql_tools.validate_session(session)
if valid_session:
   pass 
else:
    raise Exception('The DB session could not start. Check DB credentials used in the configuration file.')

#####################################
# copy events to preprocessing area #
#####################################
for j in range(len(selected_event_list)):

    # find the elements in event_list that have already been archived 
    archived_event = mysql_tools.select_event(session,data_file,selected_event_list[j],logfile)

    # if event not yet found in DB, copy to preprocessing area 
    # calculate event folder size before and after copy 
    if not archived_event: 
	size_at_origin = folder_size(event_path_list[j],logfile)
	process_path = os.path.join(proc_path,selected_event_list[j])
	temporary_path = os.path.join(temp_path,selected_event_list[j])
	try:
	    shutil.copytree(event_path_list[j],process_path,symlinks = True)
	except shutil.Error as err:
	    logfile.write('%s -- shutil.Error: %s \n' % (datetime.now(),err))
	size_at_destination = folder_size(process_path,logfile)

	# compare size before and after copy
	# if different send alert and move the folder to the failures directory
	if size_at_origin != size_at_destination:
	    msg = "Event alert: folder copied in " + proc_path + "not consistent with folder in " + event_path + "for event " + selected_event_list[j]
	    send_email(msg,recipient,sender,smtp_host,logfile)
	    try:
	        shutil.move(process_path,temporary_path)
	    except shutil.Error as err:
		logfile.write('%s -- shutil.Error: %s \n' % (datetime.now(),err))

#####################
# events processing #
#####################
foreign_stations_list = read_tools.read_txt(stations_file,CWD,logfile) 
events_to_process_path_list = glob(proc_path + '/*')

for i in events_to_process_path_list:
    os.chdir(i)

    # identify stations inside event folder
    station_folders_path_list = glob(i + '/*/')
    station_fullnames_list = [os.path.basename(os.path.normpath(k)) for k in station_folders_path_list]
    station_names_list = [k[:-19] for k in station_fullnames_list]

    for j in range(len(station_names_list)):

        # if an Italian station is found:
        # rename its thumbnail and copy to thumbnail folder
	if station_names_list[j] not in foreign_stations_list:
	    thumbnail_path = glob(station_folders_path_list[j] + "/*-thumb.jpg")
	    try:
		shutil.copy(thumbnail_path[0],os.path.join(thumbs_path,station_fullnames_list[j] + '.jpg'))
	    except IOError as err:
		logfile.write('%s -- IO.Error: %s \n' % (datetime.now(),err))

	    # rename its FITS file and add the EVENT key
	    # the value of the EVENT key corresponds to the event string  
            fits_path = glob(station_folders_path_list[j] + "/*.fit")
	    if fits_path:
		fits_filename = os.path.basename(fits_path[0])
		fits_path_renamed = station_folders_path_list[j] + 'Sum_' + fits_filename 
		event_string = os.path.basename(os.path.normpath(i))
		os.rename(fits_path[0],fits_path_renamed)
		fits_add_key(fits_path_renamed,'EVENT',event_string,'Event label',logfile)
		tar_filename = station_fullnames_list[j] + '.tar.gz' 

		# count number of files inside the folder
		folder_elements = sum([len(files) for r, d, files in os.walk(station_fullnames_list[j])])

		# create a tar file and if successful, count the number of files contained in it
		exit_code = create_tarfile(tar_filename,station_fullnames_list[j],logfile)
		if exit_code == True:
		    tar_elements = int(count_tar_elements(tar_filename,logfile))
	
		    # if the number of files in the folder equals the number of files in the tar
		    # copy the tar to the Nadir ingestion folder
		    # otherwise send an alert and move the tar file to the failures folder
		    if tar_elements == folder_elements:
		        try:
		            shutil.copy(tar_filename,ingest_path)	
		        except IOError as err:
			    logfile.write('%s -- IO.Error: %s \n' % (datetime.now(),err))
		    else:
		        msg = 'Number of frames in the tar and in the original folder do not match'
		        send_email(msg,recipient,sender,smtp_host,logfile)
			try:
			    shutil.move(tar_filename,temporary_path)
			except shutil.Error as err:
			    logfile.write('%s -- shutil.Error: %s \n' % (datetime.now(),err))

# Remove the folders in the preprocessing area
for i in events_to_process_path_list:
    shutil.rmtree(i)

logfile.close()
