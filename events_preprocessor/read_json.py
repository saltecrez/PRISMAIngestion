#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "June 2018"

import os
import json

class ReadJson(object):
    def _create_dictionary(self):
        json_config_file_path = '%s/%s' % (os.getcwd(), 'conf.json')
        config_properties = {}
        with open(json_config_file_path) as data_file:
            config_properties = json.load(data_file)
        return config_properties

    def get_email(self):
        email = self._create_dictionary().get("email")
        return email

    def get_sender(self):
        sender = self._create_dictionary().get("sender")
        return sender

    def get_smtp_host(self):
        smtp_host = self._create_dictionary().get("smtphost")
        return smtp_host

    def get_event_folder(self):
        event_folder = self._create_dictionary().get("eventfolder")
        return event_folder

    def get_db_host(self):
        db_host = self._create_dictionary().get("dbhost")
        return db_host

    def get_db_user(self):
        db_user = self._create_dictionary().get("dbuser")
        return db_user

    def get_db_pwd(self):
        db_pwd = self._create_dictionary().get("dbpwd")
        return db_pwd

    def get_db_name(self):
        db_name = self._create_dictionary().get("dbname")
        return db_name

    def get_preprocess_folder(self):
        preprocess_folder = self._create_dictionary().get("processfolder")
        return preprocess_folder

    def get_ingestion_folder(self):
        ingestion_folder = self._create_dictionary().get("ingestfolder")
        return ingestion_folder

    def get_foreign_stations(self):
        foreign_stations = self._create_dictionary().get("stations")
        return foreign_stations

    def get_thumbs_folder(self):
        thumbs_folder = self._create_dictionary().get("thumbsfolder")
        return thumbs_folder

    def get_failures_folder(self):
        failures_folder = self._create_dictionary().get("failurefolder")
        return failures_folder

if __name__ == "__main__":
    filename = 'conf.json'
    print(ReadJson(filename).get_db_pwd())

