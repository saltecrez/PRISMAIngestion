#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "December 2019"


from sqlalchemy import Column, String, Integer
from base import Base


class data_file(Base):
    __tablename__ = 'CAM'

    id = Column(Integer, primary_key=True)
    EXP_ID = Column(String(45))

    def __init__(self, EXP_ID):
        self.EXP_ID = EXP_ID
