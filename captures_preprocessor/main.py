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
from sqlalchemy import func
import multiprocessing
from multiprocessing import Pool
from multiprocessing import cpu_count
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer,select
from base import Base

CWD = os.getcwd()
logfile = open(CWD + '/' + "logfile.txt",'a')

# Read from configuration file
cnf = read_tools.read_json('conf.json',CWD,logfile) 

cameras_path = cnf['camerasfolder'];   ingest_path = cnf['ingestfolder']
db_host      = cnf['dbhost'];          db_pwd      = cnf['dbpwd']
db_user      = cnf['dbuser'];          db_name     = cnf['dbname']
tb_name      = cnf['tbname'];          thumbs_path = cnf['thumbsfolder']
thrd_nr      = int(cnf['threadsnr']);

# create captures folder list from the folder synchronized with the French server
cameras_path_list = glob(cameras_path + '/*/')

class data_file(Base):
    __tablename__ = 'PRS'

    id = Column(Integer, primary_key=True)
    file_name = Column(String(45))

    def __init__(self, file_name):
        self.file_name = file_name

def do_work(filename):
    t1 = datetime.now()
    Session = mysql_tools.mysql_session(db_user,db_pwd,db_host,db_name,logfile)
    session = Session()
    valid_session = mysql_tools.validate_session(session)
    if valid_session:
        #print("PID %d: using connection %s" % (os.getpid(), session))
        rows = session.query(data_file)
        flt = rows.filter(data_file.file_name == filename).scalar() is not None
        session.close()
        t2 = datetime.now()
        delta = t2-t1
        #print "do work performance: ", delta
        if not flt:
	    return filename
    else:
	raise Exception('The DB session could not start. Check DB credentials used in the configuration file.')

current_month = datetime.today().strftime('%Y%m')
cameras_month_path = [i + current_month for i in cameras_path_list]

for j in range(len(cameras_month_path)):
    print cameras_month_path[j]

    fits_captures = glob(cameras_month_path[j] + '/*.fit')

    for i in fits_captures:
        # JPG
        common_string = os.path.basename(os.path.splitext(os.path.normpath(i))[0])
        jpg500_name = common_string + '-500x500.jpg'
        jpg_name = common_string + '.jpg' 
        final_destination_jpg = os.path.join(thumbs_path,jpg_name)
        jpg_original_path = os.path.join(cameras_month_path[j],jpg500_name) 
        if not os.path.exists(final_destination_jpg) and os.path.exists(jpg_original_path):
            try:
                shutil.copy(jpg_original_path,final_destination_jpg)
            except shutil.Error as err:
                logfile.write('%s -- shutil.Error: %s \n' % (datetime.now(),err)) 

    # FITS 
    selects = [os.path.basename(i) + '.gz' for i in fits_captures]
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    pool = multiprocessing.Pool(processes=thrd_nr)
    not_found_in_db = pool.map_async(do_work, selects).get(timeout=300)
    pool.close()
    pool.join()

    for i in not_found_in_db:
        if i is not None:
       	    name = os.path.splitext(os.path.normpath(i))[0]
	    path = cameras_month_path[j] + '/' + name
	    try:
	        shutil.copy(path,os.path.join(ingest_path,name))
	    except shutil.Error as err:
	        logfile.write('%s -- shutil.Error: %s \n' % (datetime.now(),err))

logfile.close()
