#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "June 2018"

from read_json import ReadJson
from utilities import VerifyLinux
from utilities import LoggingClass
from processing import ArchiveFITS
from processing import CamerasPathList

log = LoggingClass('',True).get_logger()

def main():

    try:
        erifyLinux()

        rj = ReadJson()
        cam_path = rj.get_rsync_path()

        cameras_path_list = CamerasPathList(cam_path).create_list()
        # [/mnt/rsync_captures/ITER07/','/mnt/rsync_captures/ITLO01/']

        for camera in cameras_path_list:
                copyfits = ArchiveFITS(camera).copy_fits()

    except Exception as e:
        msg = "Main exception - main() -- "
        log.error("{0}{1}".format(msg,e))

if __name__ == "__main__":
   main()

