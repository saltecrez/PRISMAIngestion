#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "January 2020"

import os
import sys
import smtplib
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
                #if isfile(fp):
                    total_size += os.path.getsize(fp)
        return total_size

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

class CreateEventsString(object):
    def __init__(self, input_list):
        self.input_list = input_list

    def create_events_string(self):
        output_list = []
        for i in self.input_list:
            if i[0].isdigit() and i[8] == 'T':
                output_list.append(i)
            else:
                pass
        return output_list


if __name__ == "__main__":
    VerifyLinux()
    recipient = 'elisa.londero@inaf.it'
    sender = 'prisma@localhost' 
    smtphost = 'localhost'  
    msg = 'Severe alert'
    path = '/home/controls/workspace/development/PRISMAIngestion/events_preprocessor/sfoltisci'

    #SendEmail(msg,recipient,sender,smtphost).send_email()
    print(FolderSize(path).get_folder_size())


