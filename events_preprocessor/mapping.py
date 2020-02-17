#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "December 2019"

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from database import MySQLDatabase

Base = declarative_base()

class data_file(Base):
    __tablename__ = 'data_file'

    data_file_id = Column(Integer, primary_key=True)
    event = Column(String(60))

    def __init__(self, event):
        self.event = event
