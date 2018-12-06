from unittest import TestCase
import os
from ...db_con import connection, create_tables, db_destroy, tables
from ... import create_app
import psycopg2
from instance.config import settings

app = create_app(settings['testing'])


URL = "dbname='{}' host='{}' port='{}' user='{}' \
 password='{}'".format(app.config['DB_NAME'],
                       app.config['DB_HOST'],
                       app.config['DB_PORT'],
                       app.config['DB_USERNAME'],
                       app.config['DB_PASS'])

class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(self):
        self.app = app.test_client()
        self.app.testing = True
        self.conn = psycopg2.connect(URL)
        create_tables(self.conn, tables())
    
    @classmethod
    def tearDownClass(self):
        q1 = "DROP TABLE public.\"Incident\";"
        q2 = "DROP TABLE public.\"User\";"
        q = [q1, q2]
        db_destroy(self.conn, q)
