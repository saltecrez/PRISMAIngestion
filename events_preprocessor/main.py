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
        ep = EventPreprocessing(i) 
        ep.run()
        ep.remove_event()

if __name__ == "__main__":
   main()
