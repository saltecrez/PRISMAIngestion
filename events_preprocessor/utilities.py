#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "January 2020"

import sys
import smtplib
import email.utils
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
        print('message sent')
        server.quit()

if __name__ == "__main__":
    VerifyLinux()
    recipient = 'elisa.londero@inaf.it'
    sender = 'prisma@localhost' 
    smtphost = 'localhost'  
    msg = 'Severe alert'

    SendEmail(msg,recipient,sender,smtphost).send_email()
