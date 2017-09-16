#! /usr/bin/env python

import MySQLdb
import urlparse

class DbConnect:
    """Class to get access to DB"""

    def __init__(self, conf):
        self.sql_conn_url=urlparse.urlparse(conf.get('core', 'sql_alchemy_conn'))
        self.connect()

    def connect(self):
        self.conn = MySQLdb.connect (host = self.sql_conn_url.hostname,
                                     user = self.sql_conn_url.username,
                                     passwd = self.sql_conn_url.password,
                                     db = self.sql_conn_url.path.strip('/'),
                                     port = self.sql_conn_url.port)
        self.conn.set_character_set('utf8')
        self.cursor = self.conn.cursor()

    def close(self):
        try:
            self.conn.close()
        except:
            pass

