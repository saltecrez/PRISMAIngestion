#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "June 2018"

'''
   This script is supposed to be used for the daily 
   ingestion of event files (PRISMA project)
'''

import os
import pymysql
from glob import glob
from read_tools import read_json
from mysql_tools import mysql_session
from mysql_tools import select_event
from folder_size import folder_size 
from table_objects import data_file

#
CWD = os.getcwd()
logfile = open(CWD + '/' + "logfile.txt",'a')
cnf = read_json('conf.json',CWD,logfile) 
#
os.chdir(cnf['eventpath'])
event_path_list = list(glob(cnf['eventpath'] + '/*'))
event_list = [os.path.basename(i)[0:15] for i in event_path_list]
#
host = cnf['dbhost']; pwd = cnf['dbpwd']
user = cnf['dbuser']; schema = cnf['dbschema']
Session = mysql_session(user,pwd,host,schema)
session = Session()
#
logfile.close()
