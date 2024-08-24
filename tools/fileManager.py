import os
import secrets
import shutil
import collections
import pathlib
from pathlib import Path
from functools import cached_property


class CoreFiles:
    def __init__(self):
        self._home = Path.home()

    @cached_property
    def systemctlPath(self):
        return self._home / ".config/systemd/user"
    
    @cached_property
    def dailyBackups(self):
        return self._home / "backups"

    @cached_property
    def pzlgsm(self):
        return self._home / "pzlgsm"
    
    @cached_property
    def zcore(self):
        return self._home / "zcore"
    
    @cached_property
    def zomboidPath(self):
        return self._home / "Zomboid/"
    
    @cached_property
    def zomboidSave(self):
        return self.zomboidPath / "Saves/Multiplayer/pzserver"
    
    @cached_property
    def zomboidLogs(self):
        return self.zomboidPath / "Logs"

    @cached_property
    def serverini(self):
        return self.zomboidPath / "Server/pzserver.ini"

    @cached_property
    def processTracker(self):
        return self.zcore / "tools/skimmers/.process_tracker"
    
class LinuxFileSystem(CoreFiles):    
    def create_user_sysd_folder(self):
        Path(self.systemctlPath).mkdir(parents=True, exist_ok=True)
    
    def copy_packaged_sysd_files(self):
        self.create_user_sysd_folder()

        path = pathlib.PurePosixPath(
            f"{self._home}/zcore/install/service-files")
        
        files = [x.name for x in os.scandir(path) if x.is_file()]

        for fileName in files:
            shutil.copy2(f"{path}/{fileName}", self.systemctlPath)

        return files
    
    def get_sysd_files(self):
        return [x.name for x in os.scandir(self.systemctlPath) if x.is_file()]
    
    def alias_creation(self):
        aliasFile = self._home / ".bash_aliases"
        if not Path(aliasFile).exists():
            Path(aliasFile).touch(mode=0o700)
        with open(aliasFile, "a") as openFile:
            openFile.write(f"alias zcore='/usr/bin/python3 {self._home}/"
                f"zcore/zomboid_core.py'\nalias pzserver='"
                f"{self.pzlgsm}/pzserver'")
    
class GlobalZomboidBackups(CoreFiles):
    def create_backup_directories(self):
        (self.dailyBackups / "staging").mkdir(parents=True, exist_ok=True)
    
    def get_daily_backups(self):
        return [x.name for x in os.scandir(self.dailyBackups) if x.is_file()]
    
    def remove_oldest_backup(self, date):
        for backup in self.get_daily_backups():
            if date in backup:
                (self.dailyBackups / backup).unlink()
    
class LGSMFiles(CoreFiles):
    def create_pzlgsm_directory(self):
        Path(self.pzlgsm).mkdir(exist_ok=True)

    def create_lgsm_file(self):
        lgsmFilePath = self.pzlgsm / "linuxgsm.sh"
        Path(lgsmFilePath).touch(mode=0o700)
        return self.pzlgsm, lgsmFilePath
    
    def default_server_password(self):
        configFile = self.pzlgsm / "lgsm/config-lgsm/pzserver/common.cfg"
        password = secrets.token_urlsafe(15)
        if Path(configFile).exists():
            with open(configFile, "a") as openFile:
                openFile.write(
                    "startparameters=\"-servername ${selfname} "
                    f"-adminpassword \"{password}\"\""
                )
                
class ZomboidChunks(CoreFiles):
    def __init__(self):
        self.chunkListPath = self.zomboidPath / "Lua/chunk_lists"

    def create_chunk_directory(self):
        (self.chunkListPath).mkdir(parents=True, exist_ok=True)

    def get_chunk_file_name(self, fileName):
        chunkFilePath = self.chunkListPath / fileName
        if Path(chunkFilePath).exists():
            return chunkFilePath

    def chunk_list_to_file(self, chunkList, fileName):
        chunkFilePath = self.chunkListPath / fileName
        with open(chunkFilePath, "w") as openFile:
            for chunkFileName in chunkList:
                openFile.write(chunkFileName+"\n")
            
    def delete_chunks(self, chunkList):
        for chunkCoords in chunkList:
            chunkFileName = f"map_{chunkCoords}.bin"
            chunkFilePath = self.zomboidSave / chunkFileName
            if Path(chunkFilePath).exists():
                Path(chunkFilePath).unlink()

class ZomboidConfigurationFiles(CoreFiles):
    def open_ini_file(self):
        with open(self.serverini, "r", encoding="IBM865") as openFile:
            contents = openFile.read()
        return contents
    
    def write_ini_file(self, contents):
        with open(self._serverini, "w", encoding="IBM865") as openFile:
            openFile.write(contents)

class ZCoreFiles(CoreFiles):
    def create_process_tracker(self, name, pid):
        with open(self.processTracker, "w") as openfile:
            openfile.write(f"{name},{pid}")

    def get_process_tracker(self):
        if Path(self.processTracker).exists():
            with open(self.processTracker, "r") as openfile:
                processes = openfile.readlines()
            return processes

    def clear_process_tracker(self):
        if Path(self.processTracker).exists():
            Path(self.processTracker).unlink()

    def latest_debug_log(self):
        debugLogs = sorted(self.zomboidLogs.glob("*Debug*"))
        lastDebugLogFileIndex = len(debugLogs) - 1
        with open(debugLogs[lastDebugLogFileIndex], "r") as openLog:
            return collections.deque(openLog, 10)
        
class MiscFileFunctions(CoreFiles):
    def delete_map_sand(self):
        sandPath = self.zomboidSave / "map_sand.bin"
        if Path(sandPath).exists():
            Path(sandPath).unlink()