from pathlib import Path,PurePosixPath
from shutil import copy2
from os import scandir, remove

class LinuxFiles:
    __home = Path.home()
    __systemctlPath = PurePosixPath(__home).joinpath(".config/systemd/user")
    __rcon = PurePosixPath(__home).joinpath("rcon/rcon")
    __dailyBackups = PurePosixPath(__home).joinpath("backups")
    __pzlgsm = PurePosixPath(__home).joinpath("pzlgsm")
    __zomboid = PurePosixPath(__home).joinpath("Zomboid/")
    __zomboidLogs = PurePosixPath(__zomboid).joinpath("Logs")
    __zomboidSave = PurePosixPath(__zomboid).joinpath(
        "Saves/Multiplayer/pzserver")
    __zomboidBackups = PurePosixPath(__zomboid).joinpath("backups")
    __serverini = PurePosixPath(__zomboid).joinpath("Server/pzserver.ini")
    __accountDB = PurePosixPath(__zomboid).joinpath("db/pzserver.db")
    
    @classmethod
    def GetSysdFiles(cls):
        return [x.name for x in scandir(cls.__systemctlPath) if x.is_file()]
    
    @classmethod
    def GetDailyBackups(cls):
        return [x.name for x in scandir(cls.__dailyBackups) if x.is_file()]
    
    @classmethod
    def GetZomboidPath(cls):
        return cls.__zomboid
    
    @classmethod
    def GetDailyBackupPath(cls):
        return cls.__dailyBackups
    
    @classmethod
    def ManageLgsmFiles(cls):
        Path(cls.__pzlgsm).mkdir(exist_ok=True)
        file = cls.__pzlgsm.joinpath("linuxgsm.sh")
        Path(file).touch(mode=0o700)
        return cls.__pzlgsm, file
    
    @classmethod
    def ManageSysdFiles(cls):
        Path(cls.__systemctlPath).mkdir(parents=True, exist_ok=True)

        path = PurePosixPath(
            f"{cls.__home}/Server-Core/install/service-files")
        
        files = [x.name for x in scandir(path) if x.is_file()]

        for x in files:
            copy2(f"{path}/{x}", cls.__systemctlPath)

        return files
    
    @classmethod
    def PrepBackupDirectories(cls):
        Path(f"{cls.__home}/backups/temp").mkdir(exist_ok=True)

    @classmethod
    def RemoveOldestBackup(cls, date):
        for backup in cls.GetDailyBackups():
            if backup == date + "_backup.tar.gz":
                remove(str(cls.__dailyBackups) + "/" + backup)
