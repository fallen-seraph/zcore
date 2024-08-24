import subprocess
from subprocess import CalledProcessError
import datetime
from datetime import datetime, timedelta
import pytz
from threading import Thread

from tools import fileManager, linux_services

from utils.config import backupRetentionDays, dailyBackupTimeZone

def compress(backupPath, today, stagingPath):
    
    subprocess.run(["tar", "-czf",
        f"{backupPath}/{today}_backup.tar.gz", "-C",
        stagingPath, "."])

def backup_handler(force):
    active = None

    if not force:
        active = linux_services.get_service_status("zomboid_core.service")[1]
    
    if active == "active":
        print("Server is online. Shutdown before backing up.")
    else:
        globalBackupFiles = fileManager.GlobalZomboidBackups()
        backupPath = globalBackupFiles.dailyBackups
        stagingPath = f"{backupPath}/staging/"
        dateToDay = datetime.now(pytz.timezone(dailyBackupTimeZone))
        today = dateToDay.strftime("%d_%m_%Y-%H:%M")
        nDaysAgo = (dateToDay - timedelta(days=backupRetentionDays)).strftime(
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