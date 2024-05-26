from subprocess import run, PIPE, CalledProcessError
from datetime import date, timedelta
from tools.linux_files import LinuxFiles as files
import linux_services as services

def main():
    backupPath = files.GetDailyBackupPath()
    stagingPath = f"{backupPath}/staging/"
    dateToDay = date.today()
    today = dateToDay.strftime("%d_%m_%Y")
    threeDaysAgo = (dateToDay - timedelta(3)).strftime("%d_%m_%Y")

    services.MainServices("stop")

    try:
        run(["rsync", "-aq", "--exclude", "\'backups\'" "--delete",
            files.GetZomboidPath(), stagingPath])

        run(["tar", "-czf", f"{backupPath}/{today}_backup.tar.gz", "-C",
            stagingPath, "."])
    except CalledProcessError as e:
        print(f"An error occured: {e}.")

    services.MainServices("start")

    files.RemoveOldestBackup(threeDaysAgo)

if __name__ == '__main__':
    main()