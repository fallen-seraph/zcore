from pathlib import Path,PurePosixPath
from shutil import copy2
from os import scandir

class LinuxFiles:
    __home = Path.home()
    __systemctlPath = PurePosixPath(__home).joinpath(
        ".config/systemd/user")
    __rcon = PurePosixPath(__home).joinpath("rcon/rcon")
    __fullBackups = PurePosixPath(__home).joinpath("backups")
    __pzlgsm = PurePosixPath(__home).joinpath("pzlgsm")
    __zomboid = PurePosixPath(__home).joinpath("Zomboid/")
    __logs = PurePosixPath(__zomboid).joinpath("Logs")
    __save = PurePosixPath(__zomboid).joinpath(
        "Saves/Multiplayer/pzserver")
    __zomboidBackups = PurePosixPath(__zomboid).joinpath(
        "backups")
    __serverini = PurePosixPath(__zomboid).joinpath(
        "Server/pzserver.ini")
    __accountDB = PurePosixPath(__zomboid).joinpath(
        "db/pzserver.db")
    
    @classmethod
    def getSysdFiles(cls):
        return [x.name for x in scandir(cls.__systemctlPath) if x.is_file()]
    
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