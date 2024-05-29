import subprocess
from subprocess import CalledProcessError
import datetime
from datetime import date
from tools.linux_files import LinuxFiles as files
from configs.config import backupRetentionDays

def backup_handler():
    backupPath = files.get_daily_backup_path()
    stagingPath = f"{backupPath}/staging/"
    dateToDay = date.today()
    today = dateToDay.strftime("%d_%m_%Y")
    nDaysAgo = (dateToDay - datetime.timedelta(backupRetentionDays)).strftime("%d_%m_%Y")

    try:
        subprocess.run(["rsync", "-aq", "--exclude", "\'backups\'" "--delete",
            f"{files.get_zomboid_path()}/", stagingPath])

        subprocess.run(["tar", "-czf", f"{backupPath}/{today}_backup.tar.gz", "-C",
            stagingPath, "."])
    except CalledProcessError as e:
        print(f"An error occured: {e}.")

    files.remove_oldest_backup(nDaysAgo)