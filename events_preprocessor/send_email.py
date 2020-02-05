#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "October 2019"


import smtplib
import email.utils
from datetime import datetime
from email.mime.text import MIMEText


def send_email(message,recipient,sender,smtp_host,logfile):
    msg = MIMEText(message)
    msg['To'] = email.utils.formataddr(('To', recipient))
    msg['From'] = email.utils.formataddr(('PrismaWatchDog', sender))
    msg['Subject'] = 'Prisma alert'
    server = smtplib.SMTP(smtp_host,25)
    try:
        server.sendmail(sender, [recipient], msg.as_string())
    except smtplib.SMTPRecipientRefused as e:
        logfile.write('%s -- SMTPRecipientRefusedError: %s \n' % (datetime.now(),e))
    except smtplib.SMTPSenderRefused as e:
        logfile.write('%s -- SMTPSenderRefusedError: %s \n' % (datetime.now(),e))
    except smtplib.SMTPConnectError as e:
        logfile.write('%s -- SMTPConnectError: %s \n' % (datetime.now(),e))
    except smtplib.SMTPDataError as e:
        logfile.write('%s -- SMTPDataError: %s \n' % (datetime.now(),e))
    except smtplib.SMTPServerDisconnected as e:
        logfile.write('%s -- SMTPServerDisconnected: %s \n' % (datetime.now(),e))
    finally:
        server.quit()
