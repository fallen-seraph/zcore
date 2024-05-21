import sqlite3
from re import search

class apa_database:

    def __init__(self, file=None, readOnly=True):
        self._file = file
        self._readOnly = readOnly
        self._connector = None

    def connect(self):
        try:
            if self._readOnly:
                self._connector = sqlite3.connect(f"file:{self._file}?mode=ro", uri=True)
            else:
                self._connector = sqlite3.connect(self._file)
            return self._connector
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite database: {e}")
            return None
        
    def execute_query(self, query, params=(), fetch_one=False, fetch_all=False):
        try:
            cursor = self._connector.cursor()
            cursor.execute(query, params)
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            else:
                self._connector.commit()
                result = True
            cursor.close()
            return result
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None 

    def close(self):
        if self._connector:
            self._connector.close()
            self._connector = None

    def user_lookup(self, lookupString):
        if search("765611[0-9]{11}", lookupString):
            query = "SELECT username,steamid,lastConnection FROM whitelist WHERE steamid = %s' LIMIT 5;"
        else:
            query = "SELECT username,steamid,lastConnection FROM whitelist WHERE username = %s' LIMIT 5;"

        return self.execute_query(query, (lookupString,), True)