import subprocess
from subprocess import CalledProcessError
import datetime
from datetime import datetime, timedelta
import pytz

from tools.linux_files import LinuxFiles

from utils.config import backupRetentionDays, dailyBackupTimeZone

def backup_handler():
    backupPath = LinuxFiles.get_daily_backup_path()
    stagingPath = f"{backupPath}/staging/"
    dateToDay = datetime.now(pytz.timezone(dailyBackupTimeZone))
    today = dateToDay.strftime("%d_%m_%Y-%H:%M")
    nDaysAgo = (dateToDay - timedelta(days=backupRetentionDays)).strftime("%d_%m_%Y")

    try:
        subprocess.run(["rsync", "-aq", "--exclude", "\'backups\'" "--delete",
            f"{LinuxFiles.get_zomboid_path()}/", stagingPath])

        subprocess.run(["tar", "-czf", f"{backupPath}/{today}_backup.tar.gz", "-C",
            stagingPath, "."])
    except CalledProcessError as e:
        print(f"An error occured: {e}.")

    LinuxFiles.remove_oldest_backup(nDaysAgo)