import sqlite3
import config

def main_db_connect():
    try:
        con = sqlite3.connect(f'file:{config.server_db}?mode=ro', uri=True)
        cursor = con.cursor()
        return con, cursor
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite database: {e}")
        return

def steam_id(cur, steamid):
    try:
        #player = cur.execute(f"select username,steamid,lastConnection from whitelist where {lookup} = '{steamid}';")
        return cur.execute(f"select username,steamid,lastConnection from whitelist where steamid = '{steamid}';")

    except sqlite3.Error as e:
        print(f"Error connecting to SQLite database: {e}")
        return
    
def username(cur, username):
    try:
        return cur.execute(f"select username,steamid,lastConnection from whitelist where username = '{username}';")
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite database: {e}")
        return
    
def close_connections(con, cur):
    cur.close()
    con.close()