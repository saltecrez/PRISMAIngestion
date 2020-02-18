#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "September 2019"

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class MySQLDatabase(object):
    def __init__(self, user, pwd, host, dbname):
        self.user = user
        self.pwd = pwd
        self.host = host
        self.dbname = dbname

    def create_session(self):
        sdb = 'mysql+pymysql://%s:%s@%s/%s'%(self.user,self.pwd,self.host,self.dbname)
        engine = create_engine(sdb)
        db_session = sessionmaker(bind=engine)
        return db_session()

    def close_session(self):
        try:
            self.create_session().close()
            return True
        except Exception as e: 
            print(e)
            return False

    def validate_session(self):
        try:
            connection = self.create_session().connection()
            return True
        except:
            return False

if __name__ == "__main__":
    user = 'archa'
    pwd = 'Archa123.'
    host = 'localhost'
    dbname = 'metadata_events'
    Session = MySQLDatabase(user,pwd,host,dbname).create_session()
    print(MySQLDatabase(user,pwd,host,dbname).validate_session())
    print(MySQLDatabase(user,pwd,host,dbname).close_session())
