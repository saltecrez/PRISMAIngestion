#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "December 2019"

import subprocess
import os

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
    filein = 'testtar'     
    TarHandling(filein).create_tarfile()
    TarHandling(filein).count_tar_elements()
