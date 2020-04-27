#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "June 2018"

from read_json import ReadJson
from utilities import VerifyLinux
from utilities import LoggingClass
from processing import ArchiveFITS
from processing import CamerasPathList
from processing import MonthsString

log = LoggingClass('',True).get_logger()

def main():

    try:
        VerifyLinux()

        rj = ReadJson()
        cam_path = rj.get_rsync_path()
        mon_nr      = rj.get_months_number()
        months_list = MonthsString(mon_nr).create_strings()

        cameras_path_list = CamerasPathList(cam_path).create_list()
        # [/mnt/rsync_captures/ITER07/','/mnt/rsync_captures/ITLO01/']

        for camera in cameras_path_list:
            for month in months_list:
                copyfits = ArchiveFITS(camera,month).copy_fits()
                copyjpg = ArchiveFITS(camera,month).copy_jpg()

    except Exception as e:
        msg = "Main exception - main() -- "
        log.error("{0}{1}".format(msg,e))

if __name__ == "__main__":
   main()
