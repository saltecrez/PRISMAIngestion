#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "February 2020"

import os
from glob import glob

class CheckEventString(object):
    def __init__(self, events_folder):
        self.events_folder = events_folder

    def check_event_string(self):
        event_paths = glob(self.events_folder + '/*')
        event_strings = [os.path.basename(i)[0:15] for i in event_paths]
        output_list = []
        for i in event_strings:
            if i[0].isdigit() and i[8] == 'T':
                output_list.append(i)
            else:
                pass
        print(output_list)
        return output_list
