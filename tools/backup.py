from subprocess import run, PIPE, CalledProcessError
from datetime import date, timedelta
from tools.linux_files import LinuxFiles as files
import tools.linux_services as services

def main():
    backupPath = files.GetDailyBackupPath()
    stagingPath = f"{backupPath}/staging/"
    dateToDay = date.today()
    today = dateToDay.strftime("%d_%m_%Y")
    nDaysAgo = (dateToDay - timedelta(7)).strftime("%d_%m_%Y")

    services.MainServices("stop")

    try:
        run(["rsync", "-aq", "--exclude", "\'backups\'" "--delete",
            f"{files.GetZomboidPath()}/", stagingPath])

        run(["tar", "-czf", f"{backupPath}/{today}_backup.tar.gz", "-C",
            stagingPath, "."])
    except CalledProcessError as e:
        print(f"An error occured: {e}.")

    services.MainServices("start")

    files.RemoveOldestBackup(nDaysAgo)

if __name__ == '__main__':
    main()