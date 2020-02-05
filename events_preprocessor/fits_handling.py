#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "December 2019"


from astropy.io import fits
from datetime import datetime


def fits_add_key(fits_path,key,key_value,comment,logfile):
    try:
        hdulist = fits.open(fits_path,mode='update')
    except OSError as e:
	logfile.write('%s -- OSError: %s \n' % (datetime.now(),e))
    else:
	prihdr = hdulist[0].header
	try:
	    prihdr[key] = (key_value,comment)
            hdulist.flush()
	except KeyError as e:
	    logfile.write('%s -- KeyError: %s \n' % (datetime.now(),e))
    finally:
	hdulist.close()
