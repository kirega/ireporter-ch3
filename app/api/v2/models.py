"""Defining the models of the system"""
import json
from ...db_con import init_db_migrate, init_db
from passlib.hash import pbkdf2_sha256 as sha256
import psycopg2
from psycopg2.extras import DictCursor
import datetime
init_db_migrate()


class User ():
    def __init__(self):
        self.db = init_db()
        self.curr = self.db.cursor(cursor_factory=DictCursor)

    def save(self, first_name, last_name, other_names, phonenumber,
            email, username, password, isAdmin=False):
        """Method to save a new instance into the userdb"""

        password = self.encrypt_password(password)

        try:
            self.curr.execute("INSERT INTO public.\"User\" (first_name,last_name,other_names,phonenumber, \
                            username, email, password, isAdmin) values (%s,%s,%s,%s,%s,%s,%s,%s);",
                            (first_name, last_name, other_names, phonenumber, username, email, password, isAdmin))
        except psycopg2.IntegrityError:
            return False
        else:
            self.db.commit()
            return True

    def get_user(self, username):
        try:
            self.curr.execute("SELECT * FROM public.\"User\" WHERE username = %s;",
            [username])
        except psycopg2.ProgrammingError:
            return False
        else:
            return self.curr.fetchone()

    @staticmethod
    def encrypt_password(password):
        return sha256.hash(password)

    @staticmethod
    def check_encrypted_password(password, hashed):
        return sha256.verify(password, hashed)


class Incident():
    def __init__(self):
        self.db = init_db()
        self.curr = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    @staticmethod
    def convert(s):
        if isinstance(s,datetime.datetime):
            return s.__str__()

    def save(self,incidentType, comment, location, createdBy, images, videos):
        try:
            self.curr.execute("INSERT INTO public.\"Incident\" (createdby,comment,incidenttype,location, \
                            images, videos) values (%s,%s,%s,%s,%s,%s);",
                            (createdBy,comment,incidentType,location,images,videos))
        except psycopg2.IntegrityError :
            return False
        else:
            self.db.commit()
            return True

    def delete(self,incidentId,createdBy):
        try: 
            self.curr.execute("DELETE FROM public.\"Incident\" WHERE createdBy = %s AND id = %s ;",
            (createdBy,incidentId,))
        except psycopg2.ProgrammingError:
            return False
        else:
            self.db.commit()
            return True
            

    def get_incident(self,incidentId,createdBy):
        try: 
            self.curr.execute("SELECT * FROM public.\"Incident\" WHERE createdBy = %s AND id = %s ;",
            (createdBy,incidentId,))
        except psycopg2.ProgrammingError:
            return False
        else:
            return self.curr.fetchall()

    def get_incidents(self,createdBy):
        try: 
            self.curr.execute("SELECT * FROM public.\"Incident\" WHERE createdBy = %s ;",
            [createdBy])
        except psycopg2.ProgrammingError:
            return False
        else:
            return self.curr.fetchall()

    
