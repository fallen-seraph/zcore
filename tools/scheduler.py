import pytz
from datetime import datetime, timedelta

from tools import linux_services, lgsm, restart

from utils import config

    
def get_backup_time():
    configuredTimeZone = config.dailyBackupTimeZone
    backupHour, backupMinute = config.dailyBackupTime.split(":")
    backupTimeZone = (
        pytz.timezone(configuredTimeZone)
        if configuredTimeZone != "UTC"
        else pytz.utc
    )

    return (
        datetime.now(backupTimeZone)
        .replace(hour=int(backupHour), minute=int(backupMinute))
        .astimezone(pytz.utc)
        .strftime("%H:%M")
    )

def get_restart_interval(serverActiveTime):
    serverActiveTimeasUTC = (
        datetime.strptime(serverActiveTime, "%a %Y-%m-%d %H:%M:%S %Z")
        .astimezone(pytz.utc)
    )
    return (
        serverActiveTimeasUTC
        + timedelta(hours=config.activeHoursBeforeRestart)
    )

def trigger_restart_type(activeHours):
        currentTime = datetime.now(pytz.utc)

        if get_backup_time() == currentTime.strftime("%H:%M"):
            restart.restart_server_with_messages(
                message="a restart and a 15 minute backup", 
                triggerBackup=True
            )
        elif activeHours < currentTime:
            restart.restart_server_with_messages()
        elif currentTime.minute % 10 == 0:
            lgsm.lgsm_passthrough("checkModsNeedUpdate")

def restart_scheduler():
    isServerActive, serverActiveTime = linux_services.get_service_info(
        "zomboid_core.service")
    
    if isServerActive.split("=")[1] == "active":
        trigger_restart_type(
            get_restart_interval(
                serverActiveTime.split("=")[1]
            )
        )
    else:
        linux_services.sys_calls("stop", "zomboid_reboot.timer")

