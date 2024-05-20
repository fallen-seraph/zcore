import rcon
import database
import config
import sys
import time


def help():
    print("-cap", "--capture", "captures the current playerlist overwriting the old one")
    print("-ret", "--return", "returns player data from the instance to the main db")
    print("-rew", "--reward", "attempts to reward players who have more than x number of captures, then removes them from the db")

match sys.argv[1]:
    case "-cap" | "--capture":
        while True:
            print("Retrieving online players")
            onlinePlayers = rcon.get_online_players(config.instance_rcon_port, config.instance_rcon_password)
            print(onlinePlayers)
            
            if onlinePlayers:
                print("Connecting to participation database")
                connection, cursor = database.db_connect(config.parti_db)

                print("Updating participation database")
                database.update_parti_db(connection, cursor, onlinePlayers)

                print("Closing connections")
                database.close_connections(connection, cursor)
            else:
                print("No players online")

            print("---------------------------")
            time.sleep(300)
    case "-ret" | "--return": 
        print("Connecting to participation db")
        connection, cursor = database.db_connect(config.parti_db)
        
        print("listing participants")
        players = database.query_parti_db(cursor, False)

        print("Closing participant db connection")
        database.close_connections(connection, cursor)

        print("connecting to main player db")
        connection, cursor = database.db_connect(config.main_db)

        print("attaching instance player db")
        database.attach_instance_db(cursor, config.instance_db)

        print("updating main player db from instance player db")
        database.update_main_db(connection, cursor, players)

        print("Closing all connections")
        database.close_connections(connection, cursor)
    case "-rew" | "--reward":
        print("Retrieving online players")
        onlinePlayers = rcon.get_online_players(config.instance_rcon_port, config.instance_rcon_password)
        print(f"Online Players: {onlinePlayers}")
        
        if onlinePlayers:
            print("Connecting to participation db")
            connection, cursor = database.db_connect(config.parti_db)
            
            print("listing participants")
            participatingPlayers = database.query_parti_db(cursor, True)
            print(f"Participating Players: {participatingPlayers}")

            rewardedPlayers = []

            for player in participatingPlayers:
                if player in onlinePlayers:
                    print(f"Delievering a coin to {player}")
                    rcon.reward_participating_players(config.instance_rcon_port, config.instance_rcon_password, player)
                    rewardedPlayers.append(player)

                time.sleep(3)

            print("Marking player rewarded")
            database.update_rewarded_player(connection, cursor, rewardedPlayers)

            print("Closing participant db connection")
            database.close_connections(connection, cursor)
    case "?" | "-?" | "--help":
        help()
    case _:
        print("Unrecognized Switch.")
        help()
    