import sqlite3

def db_connect(db):
    try:
        con = sqlite3.connect(db)
        cursor = con.cursor()
        return con, cursor
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite database: {e}")
        return

def attach_instance_db(cursor, db):
    cursor.execute(f"attach database '{db}' as instance")
    
def update_main_db(con, cursor, players):
    try:
        for player in players:
            print(f"Updating {player} data")
            cursor.execute(f"update networkPlayers set (data,isDead) = \
            (SELECT instance.networkPlayers.data,instance.networkPlayers.isDead \
            from instance.networkPlayers where instance.networkPlayers.username = \
            '{player}') where networkPlayers.username = '{player}';")
            con.commit()
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite database: {e}")
        return

def query_parti_db(cursor, count):
    if count:
        command = "select name from players where count > 3 AND rewarded = 0;"
    else:
        command = "select name from players where count > 3;"
    try:
        extractedNames = []
        for name in cursor.execute(command).fetchall():
            extractedNames.append(name[0])
        return extractedNames
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite database: {e}")
        return
    
def update_parti_db(con, cursor, players):
    try:
        for player in players:
            cursor.execute(f"INSERT INTO players(name) VALUES('{player}') ON CONFLICT(name) DO UPDATE SET count=count+1;")
        con.commit()
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite database: {e}")
        return
    
def update_rewarded_player(con, cursor, players):
    try:
        for player in players:
            cursor.execute(f"update players set (rewarded) = 1 where name = '{player}'")
        con.commit()
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite database: {e}")
        return
    
def delete_from_parti_db(con, cursor, players):
    try:
        for player in players:
            cursor.execute(f"DELETE FROM players where name = '{player}'")
        con.commit()
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite database: {e}")
        return

def close_connections(con, cur):
    cur.close()
    con.close()