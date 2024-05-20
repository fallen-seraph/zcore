import sqlite3

class lgsm_commands:
    def __init__(self, file=None, password=None, steam_id=None, message=None, item=None):
        self._file = file
        self._password = password
        self._steam_id = steam_id
        self._message = message
        self._item = item