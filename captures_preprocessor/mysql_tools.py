#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "September 2019"


import pymysql
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc


def mysql_connection(host,user,password,dbname,logfile):
    try:
        db = pymysql.connect(host,user,password,dbname)
        cur = db.cursor()
        return cur, db
    except pymysql.Error as e:
        logfile.write('%s -- pymysql.Error: %s \n' % (datetime.now(),e))


def mysql_session(user,pwd,host,dbname,logfile):
    try:
        engine = create_engine('mysql+pymysql://' + user + ':' + pwd + '@' + host + '/'  + dbname)
        db_session = sessionmaker(bind=engine)
        return db_session
    except exc.SQLAlchemyError as e:
	logfile.write('%s -- sqlalchemy.Error: %s \n' % (datetime.now(),e))


def validate_session(session):
    try:
        connection = session.connection()
        return True
    except:
        return False


def select_EXPID(session,table_object,s,logfile):
    try:
        rows = session.query(table_object)
        flt = rows.filter(table_object.EXP_ID == s)
	for j in flt:
	   if j.EXP_ID:
	       return True
	   else:
	       return False
    except exc.SQLAlchemyError as e:
        logfile.write('%s -- sqlalchemy.Error: %s \n' % (datetime.now(),e))
