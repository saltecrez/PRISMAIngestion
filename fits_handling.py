#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "December 2019"


from astropy.io import fits
from datetime import datetime


def fits_add_key(fits_path,key,key_value,comment,logfile):
    try:
        hdulist = fits.open(fits_path,mode='update')
        prihdr = hdulist[0].header
        prihdr[key] = (key_value,comment)
        hdulist.flush()
        hdulist.close()
    except OSError as e:
	logfile.write('%s -- OSError: %s \n' % (datetime.now(),e))
