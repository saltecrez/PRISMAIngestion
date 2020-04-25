#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "September 2019"

import pymysql
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from utilities import LoggingClass
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
log = LoggingClass('',True).get_logger()

class MySQLDatabase(object):
    def __init__(self, user, pwd, dbname, host='localhost', port='3306'):
        self.user = user
        self.pwd = pwd
        self.host = host
        self.port = port
        self.dbname = dbname

    def _create_session(self):
        sdb = 'mysql+pymysql://%s:%s@%s:%s/%s'%(self.user,self.pwd,self.host,self.port,self.dbname)
        try:
            engine = create_engine(sdb)
            db_session = sessionmaker(bind=engine)
            return db_session()
        except Exception as e:
            msg = "Database session creation excep - MySQLDatabase._create_session -- "
            log.error("{0}{1}".format(msg,e))

    def _validate_session(self):
        try:
            connection = self._create_session().connection()
            return True
        except Exception as e:
            msg = "Database session validation excep - MySQLDatabase._validate_session -- "
            log.error("{0}{1}".format(msg,e))
            return False

    def mysql_session(self):
       Session = self._validate_session()
       if Session:
           return self._create_session() 
       else:
           exit(1)

    def close_session(self):
        try:
            self._create_session().close()
            return True
        except Exception as e: 
            msg = "Database session closing excep - MySQLDatabase.close_session -- "
            log.error("{0}{1}".format(msg,e))
            return False

class DataFile(Base):
    __tablename__ = 'PRS'

    id = Column(Integer, primary_key=True)
    file_name = Column(String(255))

    def __init__(self, file_name):
        self.file_name = file_name

class Queries(object):
    def __init__(self, session, table_object, string):
        self.session = session
        self.table_object = table_object
        self.string = string

    def match_filename(self):
        try:
            rows = self.session.query(self.table_object)
            flt = rows.filter(self.table_object.file_name == self.string)
            for j in flt:
                if j.file_name:
                    return True
                else:
                    return False
        except Exception as e:
            msg = "Match filename string excep - Queries.match_filename -- "
            log.error("{0}{1}".format(msg,e))
