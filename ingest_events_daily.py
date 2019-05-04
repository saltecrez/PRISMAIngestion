# /usr/bin/env python
# E. Londero, June 2018
# contact elisa.londero@inaf.it

# This script can be used for the daily ingestion 
# of event files (PRISMA project)

import time
import sys
import os
import shutil
import ntpath
import datetime
import MySQLdb
import re
import subprocess
import pdb
from glob import glob
from datetime import date,datetime,timedelta
from shutil import Error
from os.path import isfile,join
from astropy.io import fits
from subprocess import call

# pahts to relevant working folders
event_path='/mnt/newdata/'
processing_path='/mnt/copy_events/'
already_ingested_file='/home/ia2user/bin/eventi/already_ingested.txt'
logfile='/home/ia2user/bin/eventi/log.txt'
ingestion_path='/mnt/RDI/indirFITSprisma/'
thumb_path='/mnt/storage_prisma/Thumbnails/'

filelog=open(logfile,'a')

# define the time interval for which you
# want to do the events check
# in this case: today, yesterday and day before yesterday
month=datetime.now().strftime('%m')
year=datetime.now().year
today=datetime.now().strftime('%d')
yester_day=(date.today()-timedelta(1)).strftime('%d')
yester_month=(date.today()-timedelta(1)).strftime('%m')
yester_year=(date.today()-timedelta(1)).strftime('%Y')
dby_day=(date.today()-timedelta(2)).strftime('%d')
dby_month=(date.today()-timedelta(2)).strftime('%m')
dby_year=(date.today()-timedelta(2)).strftime('%Y')

date_today=str(year)+str(month)+str(today)+'T'
date_yesterday=str(yester_year)+str(yester_month)+str(yester_day)+'T'
date_dby=str(dby_year)+str(dby_month)+str(dby_day)+'T'

os.chdir(event_path)

t = list(glob(event_path+'/'+str(date_today)+'*/'))
y = list(glob(event_path+'/'+str(date_yesterday)+'*/'))
dby = list(glob(event_path+'/'+str(date_dby)+'*/'))
check_dates_list=t+y+dby

# read the file with the list of the 
# already ingested events
with open(already_ingested_file) as f:
	file_content = f.readlines()
file_content = [x.strip() for x in file_content]
f.close()

# Copy files from /mnt/newdata to 
# /mnt/copy_events in order to be processed
f = open(already_ingested_file,'a')
for i in check_dates_list:
	base=os.path.basename(os.path.splitext(os.path.normpath(i))[0])
	if base in file_content:
		pass
	else:
		try:
			shutil.copytree(i,os.path.join(processing_path,base),symlinks=True)
			f.write(base+"\n") 
		except IOError, e:
			filelog.write("Unable to copy directory %s" % e)
f.close()

a = list(glob(processing_path+'/*/'))

# list of foreign stations;
# the stations in this list 
# are not archived
foreign_stations = ['BEAUMONTLESVALENCE','HYERES','LESANGLES','PONTARLIER','STRASBOURG','AIXENPROVENCE','BELFORT','BESANCON','BIGUGLIA','CHALON','CHARLEVILLE','GRENOBLES','MARSEILLE','GUZET','GLUXENGLENNE','LEVERSOUD','MARIGNY','MIGENNES','ORSAY','PORTOVECCHIO','REIMS','SAINTLUPICIN','SALONDEPROVENCE','TROYES','TALENCE','CHATILLON','GRENOBLE','HOCHFELDEN','LYON','NOORDWIJK','OHP','ONETLECHATEAU','PICDUMIDI','QUERQUEVILLE','RIODEJANEIRO','SUTRIEU','BARCELONETTE','CAUSSOLS','GLUX','VALCOURT','ANGOULEME','COULOUNIEIX','EPINAL','MONTSEC','OSENBACH','URANOSCOPE','WIMEREUX','LEBLEYMARD','AUBUSSON','MOULINS','ROANNE','SAINTBONNETELVERT','SAINTJULIENDUPINET','CAEN','ARRAS','AURILLAC','BREST','BUCURESTI','CARCASSONNE','LAVAL','MANTET','MAUROUX','NANCAY','NANTES','NARBONNE','PUYDEDOME','ROCHECHOUART','TAUXIGNY','TOULOUSE','WIEN','BRUXELLES','CHAPELLEAUXLYS','ANGERS','OOSTKAPELLE','PARISOBSERVATOIRE','RENNES','VANNES','SARRALBE','ALBI','CAPPELLELAGRANDE','CAVARC','PIERRES','HENDAYE','SABRES','LILLE','KETZUR','MONTPELLIER','BELLOULETRICHARD','OLDENBURG','SAINTLUC','VANDOEUVRELESNANCY','DAX','ARETTE','CAHORS','MAUBEUGE','LEMANS','AJACCIO','DIJON','SEYSDORF','PLEUMEURBODOU','LEMANS','ROUEN','PARISMNHN','VIQUES']

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
					shutil.copy(last_jpg,os.path.join(thumb_path,jpg_renamed))
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
                                	shutil.copy(zipped,os.path.join(ingestion_path,last_zipped_station))			
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
