#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "June 2018"

from utilities import VerifyLinux
from event_selection import SelectEventString 
from event_preprocessing import CopyToPreprocessingArea
from event_preprocessing import EventPreprocessing

def main():
    VerifyLinux()

    selected = SelectEventString().get_selected_events_list()
    for i in selected:
        CopyToPreprocessingArea(i).copy_folder()
        EventPreprocessing(i).get_stations_names()

if __name__ == "__main__":
   main()
