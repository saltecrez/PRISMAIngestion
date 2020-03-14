#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "January 2020"

import os
import sys
import smtplib
import logging
import subprocess
import email.utils
import logging.handlers
from os.path import isdir
from os.path import isfile
from astropy.io import fits
from email.mime.text import MIMEText

class VerifyLinux(object):
    assert ('linux' in sys.platform), "Function can only run on Linux systems."

class LoggingClass(object):
    def __init__(self, logger_name='root', create_file=False):
        self.logger_name = logger_name
        self.create_file = create_file

    def get_logger(self):
        log = logging.getLogger(self.logger_name)
        log.setLevel(level=logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s','%Y-%m-%d %H:%M:%S')

        if self.create_file:
                fh = logging.FileHandler('file.log')
                fh.setLevel(level=logging.DEBUG)
                fh.setFormatter(formatter)

        ch = logging.StreamHandler()
        ch.setLevel(level=logging.DEBUG)
        ch.setFormatter(formatter)

        if self.create_file:
            log.addHandler(fh)

        log.addHandler(ch)
        return  log

class MissingConfParameter(Exception):
    def __init__(self, par):
        super().__init__(f"Parameter {par} not defined in configuration file")
        self.par = par

log = LoggingClass('',True).get_logger()

class SendEmail(object):
    def __init__(self, message, recipient, sender, smtphost):
        self.message = message
        self.recipient = recipient
        self.sender = sender
        self.smtphost = smtphost
    
    def send_email(self):
        msg = MIMEText(self.message)
        msg['To'] = email.utils.formataddr(('To', self.recipient))
        msg['From'] = email.utils.formataddr(('PrismaWatchDog', self.sender))
        msg['Subject'] = 'Prisma alert'
        server = smtplib.SMTP(self.smtphost, 25)
        server.sendmail(self.sender, [self.recipient], msg.as_string())
        server.quit()

class FitsAddKey(object):
    def __init__(self, fits_path, key, key_value, comment):
        self.fits_path = fits_path
        self.key = key
        self.key_value = key_value
        self.comment = comment

    def fits_add_key(self):
        hdulist = fits.open(self.fits_path,mode='update')
        prihdr = hdulist[0].header
        prihdr[self.key] = (self.key_value,self.comment)
        hdulist.flush()
        hdulist.close()

class TarHandling(object):
    def __init__(self, infolder):
        self.infolder = infolder
        self.tarfolder = self.infolder + '.tar.gz'

    def create_tarfile(self):
        '''Python's tarfile implementation is 10 times slower than Unix' tar command
           therefore I use the Unix command in this implementation'''
        exit_code = subprocess.call(['tar', '--exclude=.*', '-czvf', self.tarfolder, self.infolder])
        if exit_code == 0:
            return True
        else:
            return False

    def count_tar_elements(self):
        cmd = 'tar -tzf ' + self.tarfolder + ' | grep -vc "/$"'
        count = os.popen(cmd).read()
        print(count)
        return count

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

if __name__ == "__main__":
    VerifyLinux()
    recipient = 'elisa.londero@inaf.it'
    sender = 'prisma@localhost' 
    smtphost = 'localhost'  
    msg = 'Severe alert'
    path = '/home/controls/workspace/development/PRISMAIngestion/events_preprocessor/sfoltisci'

    #SendEmail(msg,recipient,sender,smtphost).send_email()
    print(FolderSize(path).get_folder_size())
