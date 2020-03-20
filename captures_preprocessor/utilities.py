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
        #super().__init__(f"Parameter {par} not defined in configuration file")
        self.par = par

log = LoggingClass('',True).get_logger()

class SendEmail(object):
    def __init__(self, message, recipient, sender, smtphost):
        self.message = message
        self.recipient = recipient
        self.sender = sender
        self.smtphost = smtphost
    
    def send_email(self):
        hostname = self.sender.split("@",1)[1].title() 
        msg = MIMEText(self.message)
        msg['To'] = email.utils.formataddr(('To', self.recipient))
        msg['From'] = email.utils.formataddr((hostname+'WatchDog', self.sender))
        msg['Subject'] = hostname + ' alert'
        try:
            server = smtplib.SMTP(self.smtphost, 25)
        except Exception as e:
            msg = "SMTP connection excep - SendEmail.send_email -- " 
            log.error("{0}{1}".format(msg,e))
        else:
            server.sendmail(self.sender, [self.recipient], msg.as_string())
            server.quit()
