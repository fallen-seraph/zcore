import os
import re
import shutil
import random
import secrets
import collections
from pathlib import Path
from functools import cached_property

from utils.config import Configurations

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
    
    def get_files_from_directory(self, filePath):
        return [x.name for x in os.scandir(filePath) if x.is_file()]
    
class LinuxFileSystem(CoreFiles):    
    def create_user_sysd_folder(self):
        self.systemctlPath.mkdir(parents=True, exist_ok=True)
    
    def copy_packaged_sysd_files(self):
        packagedSysFilePath = self._home / "zcore/install/service-files"
        
        packagedSYSDFiles = self.get_files_from_directory(packagedSysFilePath)

        for fileName in packagedSYSDFiles:
            shutil.copy2(f"{packagedSysFilePath}/{fileName}", self.systemctlPath)
    
    def get_sysd_files(self):
        return self.get_files_from_directory(self.systemctlPath)
    
    def alias_creation(self):
        aliasFile = self._home / ".bash_aliases"
        if not aliasFile.exists():
            aliasFile.touch(mode=0o700)
        with open(aliasFile, "a") as openFile:
            openFile.write(f"alias zcore='/usr/bin/python3 {self._home}/"
                f"zcore/zomboid_core.py'\nalias pzserver='"
                f"{self.pzlgsm}/pzserver'")
    
class GlobalZomboidBackups(CoreFiles):
    def create_backup_directories(self):
        (self.dailyBackups / "staging").mkdir(parents=True, exist_ok=True)
    
    def get_daily_backups(self):
        return self.get_files_from_directory(self.dailyBackups)
    
    def remove_oldest_backup(self, dateOfBackupsToDelete):
        for backup in self.get_daily_backups():
            if dateOfBackupsToDelete in backup:
                (self.dailyBackups / backup).unlink()
    
class LGSMFiles(CoreFiles):
    def create_pzlgsm_directory(self):
        self.pzlgsm.mkdir(exist_ok=True)

    def create_lgsm_file(self):
        lgsmFilePath = self.pzlgsm / "linuxgsm.sh"
        lgsmFilePath.touch(mode=0o700)
        return self.pzlgsm, lgsmFilePath
    
    def default_server_password(self):
        configFile = self.pzlgsm / "lgsm/config-lgsm/pzserver/common.cfg"
        password = secrets.token_urlsafe(15)
        if configFile.exists():
            with open(configFile, "a") as openFile:
                openFile.write(
                    "startparameters=\"-servername ${selfname} "
                    f"-adminpassword \"{password}\"\""
                )
                
class ZomboidChunks(CoreFiles):
    def __init__(self):
        super().__init__()
        self.chunkListPath = self.zomboidPath / "Lua/chunk_lists"

    def create_chunk_directory(self):
        self.chunkListPath.mkdir(parents=True, exist_ok=True)

    def get_chunks_from(fileObject):
        rangeList = []

        with fileObject as openFile:
            fileContents = openFile.read()
            
        rangeList = list(filter(None, fileContents.split("\n")))

        return rangeList
        
    def chunk_list_to_file(self, chunkList, fileName):
        chunkFilePath = self.chunkListPath / fileName
        with open(chunkFilePath, "w") as openFile:
            for chunkFileName in chunkList:
                openFile.write(chunkFileName+"\n")
            
    def delete_chunks(self, chunkList):
        for chunkCoords in chunkList:
            chunkFileName = f"map_{chunkCoords}.bin"
            chunkFilePath = self.zomboidSave / chunkFileName
            if chunkFilePath.exists():
                chunkFilePath.unlink()

class ZomboidConfigurationFiles(CoreFiles):
    def open_ini_file(self):
        with open(self.serverini, "r", encoding="IBM865") as openFile:
            contents = openFile.read()
        return contents
    
    def write_ini_file(self, contents):
        with open(self.serverini, "w", encoding="IBM865") as openFile:
            openFile.write(contents)

    def update_hours_for_loot_respawn(self):
        config = Configurations()
        if config.dynamicLootEnabled:
            low, high = config.dynamicLootRange
            newLootHours = random.randrange(low, high)
            iniFile = self.open_ini_file()
            oldValue = re.search("HoursForLootRespawn=.*", iniFile)
            if oldValue:
                newContents = iniFile.replace(
                    oldValue.group(0),
                    f"HoursForLootRespawn={newLootHours}"
                )
                self.write_ini_file(newContents)

class ZCoreFiles(CoreFiles):
    def create_process_tracker(self, name, pid):
        with open(self.processTracker, "w") as openfile:
            openfile.write(f"{name},{pid}")

    def get_process_tracker(self):
        if self.processTracker.exists():
            with open(self.processTracker, "r") as openfile:
                processes = openfile.readlines()
            return processes

    def clear_process_tracker(self):
        if self.processTracker.exists():
            self.processTracker.unlink()

    def latest_debug_log(self):
        debugLogs = sorted(self.zomboidLogs.glob("*Debug*"))
        lastDebugLogFileIndex = len(debugLogs) - 1
        with open(debugLogs[lastDebugLogFileIndex], "r") as openLog:
            return collections.deque(openLog, 10)
        
class MiscFileFunctions(CoreFiles):
    def delete_map_sand(self):
        sandPath = self.zomboidSave / "map_sand.bin"
        if sandPath.exists():
            sandPath.unlink()