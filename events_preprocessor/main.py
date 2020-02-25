#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "June 2018"

from utilities import VerifyLinux
from event_selection import SelectEventString 

def main():
    VerifyLinux()

    SelectEventString().get_selected_events_list()

if __name__ == "__main__":
   main()
