#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "June 2018"


def formatDate(date):
    mylist = []
    mylist.append(date)
    a=str(mylist[0])
    newdate=a.replace('-', '')
    return newdate

