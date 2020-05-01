#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "June 2018"

import os
import json
from utilities import LoggingClass
from utilities import MissingConfParameter

log = LoggingClass('',True).get_logger()

class ReadJson(object):
    def _create_dictionary(self):
        try:
            json_config_file_path = '%s/%s' % (os.getcwd(), 'conf.json')
            config_properties = {}
            with open(json_config_file_path) as data_file:
                config_properties = json.load(data_file)
            return config_properties
        except Exception as e:
            log.error("{0}".format(e))
            exit(1)
        finally:
            data_file.close()

    def get_recipient(self):
        try:
            recipient = self._create_dictionary().get("email")
            if recipient is None:
                raise MissingConfParameter('email')
            return recipient
        except MissingConfParameter as e:
            log.error("{0}".format(e))
            exit(1)

    def get_sender(self):
        try:
            sender = self._create_dictionary().get("sender")
            if sender is None:
                raise MissingConfParameter('sender')
            return sender
        except MissingConfParameter as e:
            log.error("{0}".format(e))

    def get_smtp_host(self):
        try:
            smtp_host = self._create_dictionary().get("smtp_host")
            if smtp_host is None:
                raise MissingConfParameter('smtp_host')
            return smtp_host
        except MissingConfParameter as e:
            log.error("{0}".format(e))
            exit(1)

    def get_rsync_path(self):
        try:
            rsync_path = self._create_dictionary().get("rsync_folder")
            if rsync_path is None:
                raise MissingConfParameter('rsync_folder')
            return rsync_path
        except MissingConfParameter as e:
            log.error("{0}".format(e))
            exit(1)

    def get_db_host(self):
        try:
            db_host = self._create_dictionary().get("db_host")
            if db_host is None:
                raise MissingConfParameter('db_host')
            return db_host
        except MissingConfParameter as e:
            log.error("{0}".format(e))

    def get_db_user(self):
        try:
            db_user = self._create_dictionary().get("db_user")
            if db_user is None:
                raise MissingConfParameter('db_user')
            return db_user
        except MissingConfParameter as e:
            log.error("{0}".format(e))
            exit(1)

    def get_db_pwd(self):
        try:
            db_pwd = self._create_dictionary().get("db_pwd")
            if db_pwd is None:
                raise MissingConfParameter('db_pwd')
            return db_pwd
        except MissingConfParameter as e:
            log.error("{0}".format(e))
            exit(1)

    def get_db_name(self):
        try:
            db_name = self._create_dictionary().get("db_name")
            if db_name is None:
                raise MissingConfParameter('db_name')
            return db_name
        except MissingConfParameter as e:
            log.error("{0}".format(e))
            exit(1)

    def get_db_port(self):
        try:
            db_port = self._create_dictionary().get("db_port")
            if db_port is None:
                raise MissingConfParameter('db_port')
            return db_port
        except MissingConfParameter as e:
            log.error("{0}".format(e))

    def get_ingestion_path(self):
        try:
            ingestion_path = self._create_dictionary().get("ingest_folder")
            if ingestion_path is None:
                raise MissingConfParameter('ingest_folder')
            return ingestion_path
        except MissingConfParameter as e:
            log.error("{0}".format(e))
            exit(1)

    def get_thumbs_path(self):
        try:
            thumbs_path = self._create_dictionary().get("thumbs_folder")
            if thumbs_path is None:
                raise MissingConfParameter('thumbs_folder')
            return thumbs_path
        except MissingConfParameter as e:
            log.error("{0}".format(e))
            exit(1)

    def get_failures_path(self):
        try:
            failures_path = self._create_dictionary().get("failure_folder")
            if failures_path is None:
                raise MissingConfParameter('failure_folder')
            return failures_path
        except MissingConfParameter as e:
            log.error("{0}".format(e))
            exit(1)

    def get_months_number(self):
        try:
            months_nr = self._create_dictionary().get("months_nr")
            if months_nr is None:
                raise MissingConfParameter('months_nr')
            return int(months_nr)
        except MissingConfParameter as e:
            log.error("{0}".format(e))
            exit(1)

    def get_threads_number(self):
        try:
            threads_nr = self._create_dictionary().get("threads_nr")
            if threads_nr is None:
                raise MissingConfParameter('threads_nr')
            return int(threads_nr)
        except MissingConfParameter as e:
            log.error("{0}".format(e))
            exit(1)
