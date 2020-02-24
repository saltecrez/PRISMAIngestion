#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "June 2018"

from utilities import VerifyLinux
from read_json import ReadJson
from database import MySQLDatabase

def main():
    VerifyLinux()

    rj = ReadJson()

    dbhost = rj.get_db_host()
    dbuser = rj.get_db_user()
    dbpwd = rj.get_db_pwd()
    dbname = rj.get_db_name()

    db = MySQLDatabase(dbuser, dbpwd, dbhost, dbname)
    Session = db.create_session()
    db.validate_session() 

if __name__ == "__main__":
   main()
