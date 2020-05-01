#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "June 2018"

import os
from utilities import VerifyLinux
from preprocessing import SelectEventString 
from preprocessing import EventPreprocessing
from utilities import LoggingClass

log = LoggingClass('',True).get_logger()
pwd = os.getcwd()

def main():

    try:
        VerifyLinux()

        selected = SelectEventString().get_selected_events_list()

        for i in selected:
            ep = EventPreprocessing(i) 
            ep.copy_to_preprocessing_area()
            ep.process_event()
            ep.remove_event()
            os.chdir(pwd)

    except Exception as e:
        msg = "Main exception - main() -- "
        log.error("{0}{1}".format(msg,e)) 

if __name__ == "__main__":
   main()
