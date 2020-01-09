#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "June 2018"

'''
'''

import os
import read_tools
import mysql_tools
from glob import glob
from datetime import datetime

CWD = os.getcwd()
logfile = open(CWD + '/' + "logfile.txt",'a')

# Read from configuration file
cnf = read_tools.read_json('conf.json',CWD,logfile) 
cameras_path = cnf['camerasfolder']; ingest_path    = cnf['ingestfolder']
db_host      = cnf['dbhost'];        db_pwd         = cnf['dbpwd']
db_user      = cnf['dbuser'];        db_name        = cnf['dbname']
temp_path    = cnf['failurefolder']

# create captures folder list from the folder synchronized with the French server
cameras_path_list = glob(cameras_path + '/*/')
cameras_list = [os.path.basename(os.path.normpath(i)) for i in cameras_path_list]

# create mysql database session
Session = mysql_tools.mysql_session(db_user,db_pwd,db_host,db_name,logfile)
session = Session()

current_month = datetime.today().strftime('%Y%m')
cameras_month_path = [i + current_month for i in cameras_path_list]


for i in cameras_month_path:
    fits_files = glob(i + '/*.fit')
