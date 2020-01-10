#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "January 2020"


def event_string_reader(input_list):
    output_list = []
    for i in input_list:
	if i[0].isdigit() and i[8] == 'T':
	     output_list.append(i)
	else:
	     pass
    return output_list
