#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "June 2018"

from utilities import VerifyLinux
from event_selection import SelectEventString 
from copy_folders import CopyToPreprocessingArea

def main():
    VerifyLinux()

    selected = SelectEventString().get_selected_events_list()
    for i in selected:
        CopyToPreprocessingArea(i).copy_folder()

if __name__ == "__main__":
   main()

