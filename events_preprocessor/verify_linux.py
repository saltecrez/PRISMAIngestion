#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "January 2020"


def verify_linux():
    assert ('linux' in sys.platform), "Function can only run on Linux systems."
    print('Processing...')
