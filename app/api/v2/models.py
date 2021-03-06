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
        except psycopg2.ProgrammingError:
            return False
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
        self.curr = self.db.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)

    @staticmethod
    def convert(s):
        if isinstance(s, datetime.datetime):
            return s.__str__()

    def save(self, incidentType, comment, location, createdBy, images, videos):
        try:
            self.curr.execute("INSERT INTO public.\"Incident\" (createdby,comment,incidenttype,location, \
                            images, videos) values (%s,%s,%s,%s,%s,%s);",
                              (createdBy, comment, incidentType, location, images, videos))
        except psycopg2.IntegrityError:
            return False
        except psycopg2.IntegrityError:
            return False
        else:
            self.db.commit()
            return True

    def delete(self, incidentId, createdBy):
        try:
            self.curr.execute("DELETE FROM public.\"Incident\" WHERE createdBy = %s AND id = %s ;",
                              (createdBy, incidentId,))
        except psycopg2.ProgrammingError:
            return False
        else:
            self.db.commit()
            return True

    def get_incident(self, incidentId, createdBy):
        try:
            self.curr.execute("SELECT * FROM public.\"Incident\" WHERE createdBy = %s AND id = %s ;",
                              (createdBy, incidentId,))
        except psycopg2.ProgrammingError:
            return False
        else:
            return self.curr.fetchone()

    def get_incidents(self, createdBy):
        try:
            self.curr.execute("SELECT * FROM public.\"Incident\" WHERE createdBy = %s ;",
                              [createdBy])
        except psycopg2.ProgrammingError:
            return False
        else:
            return self.curr.fetchall()
    def get_all(self):
        try:
            self.curr.execute("SELECT * FROM public.\"Incident\" ;")
        except psycopg2.ProgrammingError:
            return False
        else:
            return self.curr.fetchall()

    def validate_edit(self, incidentId, createdBy):
        try:
            self.curr.execute("SELECT * FROM public.\"Incident\" WHERE createdBy = %s AND id = %s AND status = %s ;",
                              (createdBy, incidentId, "draft",))
        except psycopg2.ProgrammingError:
            return False
        else:
            return self.curr.fetchone()

    def edit_comment(self, incidentId, comment, createdBy):
        try:
            self.curr.execute("UPDATE public.\"Incident\" SET comment = %s WHERE createdBy = %s AND id = %s AND status = %s ;",
                              (comment, createdBy, incidentId, 'draft',))
        except psycopg2.ProgrammingError:
            return False
        else:
            self.db.commit()
            return True

    def edit_location(self, incidentId, location, createdBy):
        try:
            self.curr.execute("UPDATE public.\"Incident\" SET location = %s WHERE createdBy = %s AND id = %s AND status = %s ;",
                              (location, createdBy, incidentId, 'draft',))
        except psycopg2.ProgrammingError:
            return False
        else:
            self.db.commit()
            return True

    def update_status(self, incidentId, status):
        """Updates the status of a record"""
        try:
            self.curr.execute("UPDATE public.\"Incident\" SET status = %s WHERE id = %s;",
                              (status, incidentId,))
        except psycopg2.ProgrammingError:
            return False
        except psycopg2.IntegrityError:
            return False
        else:
            self.db.commit()
            return True


class RevokeToken():

    def __init__(self):
        """
        Instantiate the connection to postgres and the psycopg2 cursor
        """
        self.db = init_db()
        self.curr = self.db.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)

    def add(self, jti):
        """
        Adds a new jti into the database
        """
        try:
            self.curr.execute("INSERT INTO public.\"RevokeToken\" (jti) \
                VALUES (%s)", (jti,))
        except psycopg2.DatabaseError:
            return False
        else:
            self.db.commit()
            return True

    def is_jwt_blacklisted(self, jti):
        """
        Finds to see if a jwt has been blacklisted.
        """
        try:
            self.curr.execute("SELECT * FROM public.\"RevokeToken\" \
                        WHERE jti = %s", (jti,))

        except psycopg2.DatabaseError:
            return False
        else:
            present = self.curr.fetchall()
            if present is None or len(present) < 1:
                return False
            return True
