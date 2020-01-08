#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "December 2019"


import os


def count_tar_elements(tarname,logfile):
    try:
	cmd = 'tar -tzf ' + tarname + ' | grep -vc "/$"' 
	count = os.popen(cmd).read()
	return count
    except subprocess.CalledProcessError as e:
	logfile.write('%s -- subprocess.CalledProcessError: %s \n' % (datetime.now(),e))
