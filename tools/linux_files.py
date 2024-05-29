import pathlib
from pathlib import Path
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
    #_serverini = pathlib.PurePosixPath(_zomboidPath).joinpath("Server/pzserver.ini")
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
                os.remove(str(cls._dailyBackups) + "/" + backup)
