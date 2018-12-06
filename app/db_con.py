import psycopg2
import os

DB_HOST = os.environ.get('DB_HOST')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASS= os.environ.get('DB_PASS')
DB_NAME= os.environ.get('DB_NAME')
DB_PORT= os.environ.get('DB_PORT')

URL = "dbname='{}' host='{}' port='{}' user='{}' \
 password='{}'".format(DB_NAME,DB_HOST,DB_PORT,DB_USERNAME,DB_PASS)

def tables():
    table1 = """CREATE TABLE IF NOT EXISTS "User"
    (   id serial PRIMARY KEY,
        first_name varchar(50) NOT NULL,
        last_name  varchar(50) NOT NULL,
        other_names varchar(50) ,
        phonenumber varchar(50) NOT NULL, 
        username varchar(64) UNIQUE,
        email varchar(120) UNIQUE,
        password varchar(256) NOT NULL,
        isAdmin boolean DEFAULT FALSE,
        registeredOn timestamp DEFAULT now()
    );"""

    table2 = """CREATE TABLE IF NOT EXISTS "Incident"
    (   id serial PRIMARY KEY,
        user_id INTEGER,
        comment varchar(255) NOT NULL,
        incidentType varchar(25) check(incidentType in ('red-flag', 'intervention')),
        location varchar(50),
        status varchar(50) DEFAULT 'draft' check(status in ('draft','under-investigation','resolved','rejected')), 
        images bytea,
        videos bytea,
        createdOn timestamp DEFAULT now(),
        FOREIGN KEY (user_id) REFERENCES public."User" (id)
    );"""
    table_queries = [table1,table2]
    return table_queries

def connection(url):
    conn = psycopg2.connect(URL)
    return conn

def init_db():
    conn = connection(URL)
    return conn

def create_tables():
    conn = connection(URL)
    curr = conn.cursor()
    queries =  tables()
    for i in queries:
        curr.execute(i)
    conn.commit()

def init_db_migrate():
    create_tables()
