#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "December 2019"


import os
import subprocess


'''Python's tarfile implementation is 10 times slower than Unix' tar command
therefore I use the Unix command in this implementation'''


def create_tarfile(outfile,source,logfile):
    try:
	exit_code = subprocess.call(['tar', '--exclude=.*', '-czvf', outfile, source])
	if exit_code == 0:
	    return True
	else:
	    return False
    except subprocess.CalledProcessError as e:
	logfile.write('%s -- subprocess.CalledProcessError: %s \n' % (datetime.now(),e))
