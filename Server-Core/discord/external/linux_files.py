import os

class linux_files:
    def __init__(self):
        self.__home = os.path.expanduser('~')
        self.__systemctlPath = f"{self.__home}/.config/systemd/user"
        self.__rcon = f"{self.__home}/rcon/rcon"
        self.fullBackups = f"{self.__home}/backups"

        self.zomboid = f"{self.__home}/Zomboid/"
        self.logs = f"{self.zomboid}/Logs"
        self.save = f"{self.zomboid}/Saves/Multiplayer/pzserver"
        self.zomboidBackups = f"{self.zomboid}/backups"

        self.serverini = f"{self.zomboid}/Server/pzserver.ini"
        self.accountDB = f"{self.zomboid}/db/pzserver.db"