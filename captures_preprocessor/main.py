#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "June 2018"

from utilities import VerifyLinux
from utilities import LoggingClass

log = LoggingClass('',True).get_logger()

def main():

    try:
        VerifyLinux()

    except Exception as e:
        msg = "Main exception - main() -- "
        log.error("{0}{1}".format(msg,e))

if __name__ == "__main__":
   main()

