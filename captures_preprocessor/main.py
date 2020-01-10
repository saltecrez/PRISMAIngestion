#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "June 2018"

'''
'''

import os
import shutil
import read_tools
import mysql_tools
from glob import glob
from datetime import datetime
from table_objects import data_file

CWD = os.getcwd()
logfile = open(CWD + '/' + "logfile.txt",'a')

# Read from configuration file
cnf = read_tools.read_json('conf.json',CWD,logfile) 

cameras_path = cnf['camerasfolder'];   ingest_path = cnf['ingestfolder']
db_host      = cnf['dbhost'];          db_pwd      = cnf['dbpwd']
db_user      = cnf['dbuser'];          db_name     = cnf['dbname']
thumbs_path = cnf['thumbsfolder']

# create captures folder list from the folder synchronized with the French server
cameras_path_list = glob(cameras_path + '/*/')

# create mysql database session
Session = mysql_tools.mysql_session(db_user,db_pwd,db_host,db_name,logfile)
session = Session()
valid_session = mysql_tools.validate_session(session)
if valid_session:
   pass
else:
    raise Exception('The DB session could not start. Check DB credentials used in the configuration file.')

current_month = datetime.today().strftime('%Y%m')
cameras_month_path = [i + current_month for i in cameras_path_list]

for j in range(len(cameras_month_path)):

    # FITS and Thumbnails archiviation
    fits_captures = glob(cameras_month_path[j] + '/*.fit')
    for i in fits_captures:

	# JPG
	common_string = os.path.basename(os.path.splitext(os.path.normpath(i))[0])
	jpg500_name = common_string + '-500x500.jpg'
	jpg_name = common_string + '.jpg' 
	final_destination_jpg = os.path.join(thumbs_path,jpg_name)
	jpg_original_path =  cameras_month_path[j] + '/' + jpg500_name
	if not os.path.exists(final_destination_jpg):
	    try:
		shutil.copy(jpg_original_path,final_destination_jpg)
	    except shutil.Error as err:
		logfile.write('%s -- shutil.Error: %s \n' % (datetime.now(),err)) 

        # FITS
	fits_name = os.path.basename(i)
	archived_capture = mysql_tools.select_EXPID(session,data_file,fits_name,logfile)
	if not archived_capture:
       	    try:
	        shutil.copy(i,os.path.join(ingest_path,fits_name))
	    except shutil.Error as err:
	        logfile.write('%s -- shutil.Error: %s \n' % (datetime.now(),err))

logfile.close()
