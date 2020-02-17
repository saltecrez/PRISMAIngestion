#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "September 2019"

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class MySQLDatabase(object):
    def __init__(self, user, password, host, dbname):
        self.user = user
        self.password = password
        self.host = host
        self.dbname = dbname

    def mysql_session(self):
        engine = create_engine('mysql+pymysql://'+self.user+':'+self.password+'@'+self.host+'/'+ self.dbname)
        db_session = sessionmaker(bind=engine)
        return db_session()

    def validate_session(self):
        try:
            connection = self.mysql_session().connection()
            return True
        except:
            return False

if __name__ == "__main__":
    user = 'archa'
    pwd = 'Archa123.'
    host = 'localhost'
    dbname = 'metadata_events'
    Session = MySQLDatabase(user,pwd,host,dbname).mysql_session()
    print(MySQLDatabase(user,pwd,host,dbname).validate_session())
