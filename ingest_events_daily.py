# /usr/bin/env python
# E. Londero, June 2018
# contact elisa.londero@inaf.it

# This script is supposed to be used for the daily 
# ingestion of event files (PRISMA project)

import time
import sys
import os
import shutil
import ntpath
import datetime
import json

#import MySQLdb
#import re
#import subprocess
#import pdb
#from datetime import *
#from glob import glob
##from shutil import Error
#from os.path import isfile,join
##from astropy.io import fits
#from subprocess import call

# Load input file defining the paths
CWD=os.getcwd()
def readJson(filename):
    JSON_CONFIG_FILE_PATH='%s/%s' % (CWD, 'config.json')
    CONFIG_PROPERTIES={}
    try:
        with open(JSON_CONFIG_FILE_PATH) as data_file:
            CONFIG_PROPERTIES=json.load(data_file)
        return CONFIG_PROPERTIES
    except IOError as e:
            print e 
            print 'IOError: Unable to open config.json. Terminating execution.'
            exit(1)

cnf = readJson('config.json') 
filelog=open(cnf['logfile'],'a')

# Date interval range
def formatDate(date):
    mylist = []
    mylist.append(date)
    a=str(mylist[0])
    newdate=a.replace('-', '')
    return newdate

today=formatDate(datetime.date.today())+'T'
yester=formatDate(datetime.date.today())+'T'
dby=formatDate(datetime.date.today())+'T'

# Read foreign and italian staions list
def readStations(filename):
    filepath='%s/%s' % (CWD, filename)
    mylist = []
    try:
        with open(filepath, 'r') as filehandle:
            for line in filehandle:
               # remove linebreak which is the last character of the string
               currentPlace = line[:-1]
               mylist.append(currentPlace)
        return mylist
    except IOError as e:
        print e
        print 'IOError: Unable to open stations list file. Terminating execution.'
        exit(1)

foreign_stations = readStations('foreign_stations.txt')
italian_stations = readStations('italian_stations.txt')

os.chdir(cnf['event_path'])

# Create event paths
t = list(glob(cnf['event_path']+'/'+str(date_today)+'*/'))
y = list(glob(cnf['event_path']+'/'+str(date_yesterday)+'*/'))
dby = list(glob(cnf['event_path']+'/'+str(date_dby)+'*/'))
check_dates_list=t+y+dby

# read the file with the list of the 
# already ingested events
f = open(cnf['already_ingested_file'],'a')
with open(cnf['already_ingested_file']) as f:
	file_content = f.readlines()
file_content = [x.strip() for x in file_content]
f.close()

# Copy files from /mnt/newdata to 
# /mnt/copy_events in order to be processed
for i in check_dates_list:
	base=os.path.basename(os.path.splitext(os.path.normpath(i))[0])
	if base in file_content:
		pass
	else:
		try:
			shutil.copytree(i,os.path.join(cnf['processing_path'],base),symlinks=True)
			f.write(base+"\n") 
		except IOError, e:
			filelog.write("Unable to copy directory %s" % e)
f.close()

a = list(glob(cnf['processing_path']+'/*/'))

# file processing in /mnt/copy_events
# add the EVENT key to the fits header 
# set the value of the EVENT key
# recreate a tar file
# copy the *tar.gz to the ingestion folder
# copy the thumbnail to the thumbnail folder
list_targz=[]
for i in a:
        last=os.path.basename(os.path.normpath(i))
	event_string=last[0:15]
	os.chdir(i)
        b = glob(i+"/*/") 
        for j in b:
		station_full=os.path.basename(os.path.normpath(j))
		station=station_full[:-19]
		if station in foreign_stations:
			continue
		else:
			os.chdir(j) 
			d = glob(j+"/*-thumb.jpg")
			if d:
				last_jpg=os.path.basename(os.path.normpath(d[0]))
				jpg_renamed=station_full+'.jpg'
				try:
					shutil.copy(last_jpg,os.path.join(cnf['thumb_path'],jpg_renamed))
				except IOError, e:
					filelog.write("Unable to copy file %s" % e)
                	c = glob(j+"/*.fit")
			if c:
				last_fit=os.path.basename(os.path.normpath(c[0]))
				fit_renamed=os.rename(last_fit,'Sum_'+last_fit)	
				l = glob(j+"/*.fit")
				hdulist = fits.open(l[0],mode='update')
				prihdr = hdulist[0].header
				prihdr['EVENT'] = (event_string,'Event label')
				hdulist.flush()
				hdulist.close()
				os.chdir('..')
				pro=subprocess.call(['tar', '-czvf', station_full+'.tar.gz', station_full])
				zipped=station_full+'.tar.gz'
				list_targz.append(zipped)
				last_zipped_station=os.path.basename(os.path.normpath(zipped))
				try:
                                	shutil.copy(zipped,os.path.join(cnf['ingestion_path'],last_zipped_station))			
				except IOError, e:
					filelog.write("Unable to copy file %s" % e)

# wait until the files have been 
# ingested before checking the DB
time.sleep(360)

# connect to DB
db = MySQLdb.connect("localhost","ia2user","Asi73369.","prisma")
cur = db.cursor()
select_file_info_id='select file_info_id from web_2 where file_name=%s;'

# check if the files produced have 
# already been ingested; if so, 
# append them to a list
already_in_db=[]
for l in list_targz:
	cur.execute(select_file_info_id, [l])
	resultDB=cur.fetchall()
	if cur.rowcount==0:
		try:
			filelog.write('TARGZ ** File %s never detected before\n' % (l))
		except Exception as e:
			e = sys.exc_info()
			filelog.write(str(e[1]))
	elif cur.rowcount!=0:
		try:
			filelog.write('File %s already archived\n' % (l))
			already_in_db.append(l)
		except Exception as e:
			e = sys.exc_info()
			filelog.write(str(e[1]))

# if the list of the already ingested 
# files coincides with the list of the 
# *.tar.gz file just produced, remove 
# the folders in /mnt/copy_events
already_in_db.sort()
list_targz.sort()
if already_in_db==list_targz:
	for i in a:
		try:
			shutil.rmtree(i)
		except Exception as e:
			e = sys.exc_info()
			filelog.write(str(e[1]))
else:
	filelog.write('Something went wrong, email was sent')
	os.system("mutt -s 'PRISMA event ingestion error' -c elisa.londero@inaf.it < '/home/ia2user/bin/eventi/message.txt' ")

filelog.close()
