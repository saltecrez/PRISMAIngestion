#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "December 2019"

from mapping import data_file
from database import MySQLDatabase

class Queries(object):
    def __init__(self, session, table_object, string):
        self.session = session
        self.table_object = table_object
        self.string = string

    def match_event(self):
        rows = self.session.query(self.table_object)
        flt = rows.filter(self.table_object.event == self.string)
        for j in flt:
            if j.event:
                print(True)
                return True
            else:
                print(False)
                return False


if __name__ == "__main__":
    user = 'archa'
    pwd = 'Archa123.'
    host = 'localhost'
    dbname = 'metadata_events'
    session = MySQLDatabase(user,pwd,host,dbname).mysql_session()
    Queries(session,data_file,'20170621T221847').match_event()

