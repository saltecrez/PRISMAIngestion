#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "June 2018"

from utilities import VerifyLinux
from utilities import LoggingClass

from read_json import ReadJson
from processing import CaptureFoldersList
from processing import MonthsString
from processing import DoWork

log = LoggingClass('',True).get_logger()

def main():

    try:
        VerifyLinux()

        rj = ReadJson()
        cam_path = rj.get_rsync_path()
        mon_nr = rj.get_months_number()
        captures_folder_list = CaptureFoldersList(cam_path).create_list()
        months_list = MonthsString(mon_nr).create_strings()
        print(captures_folder_list)
        print(months_list)
        filename1 = 'ITCL01_20190326T090553_UT-0.fit.gz'
        filename2 = 'ITVA01_20200411T081504_UT-0.fit.gz'
        test_work = DoWork(filename2).do_work()
        print(test_work)

    except Exception as e:
        msg = "Main exception - main() -- "
        log.error("{0}{1}".format(msg,e))

if __name__ == "__main__":
   main()

