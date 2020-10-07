import sqlite3
import base64
import hashlib

from pydantic import BaseModel
from sqlite3 import Error

class AuthDB:

    def __init__(self, email: str, password: str, token: str, number_of_vehicles: str):
        self.connection = self.createConnection()
        self.email = email
        self.password = str(hashlib.sha224(password.encode('utf-8')).hexdigest())
        self.token = token
        self.number_of_vehicles = number_of_vehicles

    def createConnection(self):

        try:
            new_connection = sqlite3.connect('databases/auth_token.db')
        except Error as e:
            print(e)
        
        if new_connection is not None:
            try:
                cursor = new_connection.cursor()
                cursor.execute(''' CREATE TABLE IF NOT EXISTS auth_token(
                                            email text PRIMARY KEY, 
                                            password text NOT NULL, 
                                            token text NOT NULL, 
                                            number_of_vehicles integer NOT NULL);''')
            except Error as e:
                print(e)
        else:
            print("Error! Can't build database!")

        return new_connection

    def insertToDatabase(self):
        cursor = self.connection.cursor()
        cursor.execute(''' INSERT INTO auth_token(email, password, token, number_of_vehicles) 
                                VALUES(?,?,?,?)''', (self.email, self.password, self.token, self.number_of_vehicles))
        self.connection.commit()

        #Returns the attribute of the Cursor object to get back the  generated UD
        return cursor.lastrowid

    def removeFromDatabase(self, email):
        cursor = self.connection.cursor()
        cursor.execute(''' DELETE FROM auth_token WHERE email=?''', (email,))

        self.connection.commit()

        return cursor.lastrowid

    def searchByEmail(self, email):
        cursor = self.connection.cursor()
        cursor.execute(''' SELECT email FROM auth_token WHERE email=?''', (email,))
        if cursor.fetchall():
            return True
        return False

    def updateDataEntry(self):
        cursor = self.connection.cursor()
        cursor.execute(''' UPDATE auth_token SET password=?, token=?, number_of_vehicles=? WHERE email=?''', (self.password, self.token, self.number_of_vehicles, self.email))

        self.connection.commit()
        return cursor.lastrowid
    
    def printContents(self):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT email FROM auth_token WHERE email NOT NULL''')
        for row in cursor.fetchall():
            print(row[1])
    
    def addVehicle(self):
        self.number_of_vehicles = self.number_of_vehicles + 1

    def removeVehicle(self):
        self.number_of_vehicles = self.number_of_vehicles - 1

        if self.number_of_vehicles < 0:
            self.number_of_vehicles = 0

