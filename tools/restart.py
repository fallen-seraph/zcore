import pytz
import random
import time
import sys
import re
from datetime import datetime, timedelta

from tools import linux_services, lgsm, backup, discord
from tools.delay import DelayCalculator
from tools.linux_files import LinuxFiles

from utils import config


def send_message(fullMessage):
    print(fullMessage)
    lgsm.send_server_message(fullMessage)
    discord.discord_player_notifications(fullMessage)

def instant_restart():
    linux_services.main_services("restart")

def stop_and_start(triggerBackup, stop):
    linux_services.main_services("stop")
    LinuxFiles.delete_map_sand() 

    if triggerBackup:
        backup.backup_handler()
        if config.dynamicLootEnabled:
            dynamic_loot()

    #aggregated.log

    if not stop:
        linux_services.main_services("start")

def cancel_restart():
    linux_services.sys_calls("stop", "zomboid_reboot.service")
    send_message("Reboot cancelled")

def dynamic_loot():
    low, high = config.dynamicLootRange
    random.randrange(low, high)
    iniFile = LinuxFiles.open_ini_file()
    oldValue = re.search("HoursForLootRespawn=.*", iniFile)
    if oldValue:
        newContents = iniFile.replace(oldValue.group(0),
            "HoursForLootRespawn=10")
        LinuxFiles.write_ini_file(newContents)

def restart_handler(message, delay, triggerBackup, stop):
    try:
        ShutdownDelay = DelayCalculator(int(delay))
    except ValueError as verr:
            sys.exit(f"{verr}")
    except TypeError:
        ShutdownDelay = DelayCalculator()

    print(f"Restarting the server in {ShutdownDelay.totalDelay}")

    if message:
        baseMessage = f"Restarting the server for {message}"
    else:
        baseMessage = "Restarting the server for a scheduled reboot"

    reboot_intervals = ShutdownDelay.get_all_intervals()
    for x in reboot_intervals:
        if not x == 1:
            fullMessage = " ".join([baseMessage, f"in {x} minutes."])
            send_message(fullMessage)
            time.sleep(300)
        else:
            fullMessage = " ".join([baseMessage, "in 1 minute."])
            send_message(fullMessage)
            time.sleep(30)

    lgsm.save_server()
    
    time.sleep(30)

    stop_and_start(triggerBackup, stop)

def restart_schedular():
    active, activeTime = linux_services.get_service_info(
        "zomboid_core.service")
    active = active.split("=")[1]
    
    if active == "active":
        backupHour, backupMinute = config.dailyBackupTime.split(":")

        if not config.dailyBackupTimeZone == "UTC":
            backupTimeZone = pytz.timezone(config.dailyBackupTimeZone)
            backupTime = datetime.now(backupTimeZone).replace(hour=int(
                backupHour), minute=int(backupMinute)).astimezone(pytz.utc)
        else:
            backupTime = datetime.now(pytz.utc).replace(hour=int(backupHour),
                minute=int(backupMinute))
        
        currentTime = datetime.now(pytz.utc)
        activeTime = activeTime.split("=")[1]
        activeTime = datetime.strptime(activeTime,
            "%a %Y-%m-%d %H:%M:%S %Z").astimezone(pytz.utc)
        sixHoursAfterStart = activeTime + timedelta(hours=6)

        if currentTime.strftime("%H:%M") == backupTime.strftime("%H:%M"):
            print("Restart and 15 minute backup")
            restart_handler("a restart and a 15 minute backup",
                None, True, False)
        elif sixHoursAfterStart < currentTime:
            print("6 hour reboot")
            restart_handler(None, None, False, False)
        else:
            print("mod update")
            lgsm.lgsm_passthrough("checkModsNeedUpdate")