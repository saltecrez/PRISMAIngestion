#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "January 2020"

import os
import sys
import smtplib
import subprocess
import email.utils
from os.path import isdir
from os.path import isfile
from astropy.io import fits

from email.mime.text import MIMEText

class VerifyLinux(object):
    assert ('linux' in sys.platform), "Function can only run on Linux systems."

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

if __name__ == "__main__":
    VerifyLinux()
    recipient = 'elisa.londero@inaf.it'
    sender = 'prisma@localhost' 
    smtphost = 'localhost'  
    msg = 'Severe alert'
    path = '/home/controls/workspace/development/PRISMAIngestion/events_preprocessor/sfoltisci'

    #SendEmail(msg,recipient,sender,smtphost).send_email()
    print(FolderSize(path).get_folder_size())
