#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "September 2019"

from read_json import ReadJson

rj = ReadJson()

def _get_cameras_path(self):
    try:
        cameras_path = rj.get_rsync_path()
        cameras_path_list = glob(cameras_path + '/*/')
        return cameras_path_list
    except Exception as e:
        msg = "Cameras path list creation excep - xxx._get_cameras_path --"
        log.error("{0}{1}".format(msg,e))

def _get_all_months(self):
    try:
        mnr = rj.get_months_number()
        all_months = [(datetime.now() + timedelta(-30*i)).strftime('%Y%m') for i in range(mnr)]
    except Exception as e:
        msg = "Total months calculation excep - xxx._get_all_months --"
        log.error("{0}{1}".format(msg,e))
