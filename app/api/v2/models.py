"""Defining the models of the system"""

from ...db_con import create_tables, init_db

create_tables()

class User ():
    def __init__(self):
        self.db = init_db()
    
    def save(self):
        pass
    

class Incident():
    def __init__(self):
        self.db = init_db()
    def save(self):
        pass
    def get_incident(self):
        pass
    def get_incidents(self):
        pass
    
