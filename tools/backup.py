import re
import pytz
import random
import subprocess
from subprocess import CalledProcessError
import datetime
from datetime import datetime, timedelta
from threading import Thread

from file_manager import ZomboidConfigurationFiles, GlobalZomboidBackups
from linux_services import get_service_status
from utils import Configurations

config = Configurations()

def compress(backupPath, today, stagingPath):
    subprocess.run(["tar", "-czf",
        f"{backupPath}/{today}_backup.tar.gz", "-C",
        stagingPath, "."])

def dynamic_loot():
    zomboidConfigFiles = ZomboidConfigurationFiles()
    low, high = config.dynamicLootRange
    newLootHours = random.randrange(low, high)
    iniFile = zomboidConfigFiles.open_ini_file()
    oldValue = re.search("HoursForLootRespawn=.*", iniFile)
    if oldValue:
        newContents = iniFile.replace(oldValue.group(0),
            f"HoursForLootRespawn={newLootHours}")
        zomboidConfigFiles.write_ini_file(newContents)

def backup_handler(force):

    if config.dynamicLootEnabled:
        dynamic_loot()

    active = None

    if not force:
        active = get_service_status("zomboid_core.service")[1]
    
    if active == "active":
        print("Server is online. Shutdown before backing up.")
    else:
        globalBackupFiles = GlobalZomboidBackups()
        backupPath = globalBackupFiles.dailyBackups
        stagingPath = f"{backupPath}/staging/"
        dateToDay = datetime.now(pytz.timezone(config.dailyBackupTimeZone))
        today = dateToDay.strftime("%d_%m_%Y-%H:%M")
        nDaysAgo = (dateToDay - timedelta(days=config.backupRetentionDays)).strftime(
            "%d_%m_%Y")

        try:
            subprocess.run(["rsync", "-aq", "--exclude", "backups",
                "--delete", f"{globalBackupFiles.zomboidPath}/", stagingPath])
            
            thread = Thread(target=compress, args=(backupPath, today, stagingPath))
            thread.start()
        except CalledProcessError as e:
            print(f"An error occured: {e}.")

        globalBackupFiles.remove_oldest_backup(nDaysAgo)

        return thread