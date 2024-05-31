import pathlib
from pathlib import Path
import secrets
import shutil
import os

class LinuxFiles:
    _home = Path.home()
    _systemctlPath = pathlib.PurePosixPath(_home).joinpath(
        ".config/systemd/user")
    _dailyBackups = pathlib.PurePosixPath(_home).joinpath("backups")
    _pzlgsm = pathlib.PurePosixPath(_home).joinpath("pzlgsm")
    _zomboidPath = pathlib.PurePosixPath(_home).joinpath("Zomboid/")
    #_zomboidLogs = pathlib.PurePosixPath(_zomboidPath).joinpath("Logs")
    _zomboidSave = pathlib.PurePosixPath(_zomboidPath).joinpath(
        "Saves/Multiplayer/pzserver")
    #_zomboidBackups = pathlib.PurePosixPath(_zomboidPath).joinpath("backups")
    _serverini = pathlib.PurePosixPath(_zomboidPath).joinpath("Server/pzserver.ini")
    #_accountDB = pathlib.PurePosixPath(_zomboidPath).joinpath("db/pzserver.db")

    @property
    def home(self):
        return pathlib.PurePosixPath(self._home)
    
    @property
    def systemctlPath(self):
        return self.systemctlPath
    
    @property
    def pzlgsm(self):
        return self._pzlgsm
    
    @property
    def dailyBackups(self):
        return self._dailyBackups
    
    @property
    def zomboidPath(self):
        return self._zomboidPath
    
    @property
    def zomboidSave(self):
        return self._zomboidSave
    
    @property
    def serverini(self):
        return self._serverini
    
    @classmethod
    def get_home(cls):
        return cls._home
    
    @classmethod
    def get_pzlgsm(cls):
        return cls._pzlgsm
    
    @classmethod
    def get_zomboid_path(cls):
        return cls._zomboidPath
    
    @classmethod
    def get_daily_backup_path(cls):
        return cls._dailyBackups
    
    @classmethod
    def get_sysd_files(cls):
        return [x.name for x in os.scandir(cls._systemctlPath) if x.is_file()]
    
    @classmethod
    def get_daily_backup_files(cls):
        return [x.name for x in os.scandir(cls._dailyBackups) if x.is_file()]
    
    @classmethod
    def manage_lgsm_files(cls):
        Path(cls._pzlgsm).mkdir(exist_ok=True)
        file = cls._pzlgsm.joinpath("linuxgsm.sh")
        Path(file).touch(mode=0o700)

        return cls._pzlgsm, file
    
    @classmethod
    def default_server_password(cls):
        configFile = cls._pzlgsm.joinpath("lgsm/config-lgsm/pzserver/pzserver.cfg")
        password = secrets.token_urlsafe(15)
        if Path(configFile).exists():
            with open(configFile, "a") as openFile:
                openFile.write(f"adminpassword={password}")

    @classmethod
    def manage_sysd_files(cls):
        Path(cls._systemctlPath).mkdir(parents=True, exist_ok=True)

        path = pathlib.PurePosixPath(
            f"{cls._home}/Server-Core/install/service-files")
        
        files = [x.name for x in os.scandir(path) if x.is_file()]

        for x in files:
            shutil.copy2(f"{path}/{x}", cls._systemctlPath)

        return files
    
    @classmethod
    def prep_backup_directories(cls):
        Path(f"{cls._dailyBackups}/staging").mkdir(parents=True,
            exist_ok=True)

    @classmethod
    def remove_oldest_backup(cls, date):
        for backup in cls.get_daily_backup_files():
            if backup == date + "_backup.tar.gz":
                Path(cls._dailyBackups.joinpath(backup)).unlink()

    @classmethod
    def prep_chunk_directory(cls):
        Path(cls._zomboidPath.joinpath("Lua/chunk_lists")).mkdir(
            parents=True, exist_ok=True)

    @classmethod
    def get_exported_list(cls, fileName):
        chunkFile = cls._zomboidPath.joinpath(f"Lua/chunk_lists/{fileName}")
        if Path(chunkFile).exists():
            return chunkFile

    @classmethod
    def chunks_to_file(cls, rangeList, fileName):
        newFile = cls._zomboidPath.joinpath(f"Lua/chunk_lists/{fileName}")
        with open(newFile) as openFile:
            for fileName in rangeList:
                openFile.write(fileName+"\n")
            
    @classmethod
    def delete_chunks(cls, rangeList):
        for row in rangeList:
            Path(cls._zomboidSave.joinpath(row)).unlink()

    @classmethod
    def alias_creation(cls):
        file = cls._home.joinpath(".bash_aliases")
        if not Path(file).exists():
            Path(file).touch(mode=0o700)
        with open(file, "a") as openFile:
            openFile.write(f"alias zcore='/usr/bin/python3 {cls._home}/"
                f"Server-Core/zomboid_core.py'\nalias pzserver='"
                f"{cls._pzlgsm}/pzserver'")

    @classmethod
    def open_ini_file(cls):
        with open(cls._serverini, "r", encoding="IBM865") as openFile:
            contents = openFile.read()
        return contents
    
    @classmethod
    def write_ini_file(cls, contents):
        with open(cls._serverini, "w", encoding="IBM865") as openFile:
            openFile.write(contents)