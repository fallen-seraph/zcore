import os
import re
import sys
import time
import pytz
import random
import signal
from datetime import datetime, timedelta

from tools import linux_services, lgsm, backup, discord
from tools.delay import DelayCalculator
from tools.linux_files import LinuxFiles

from utils import config


def send_message(fullMessage):
    lgsm.send_server_message(fullMessage)
    discord.discord_player_notifications(fullMessage)

def instant_restart():
    linux_services.core_service("restart")

def cancel_pending_restart(message):
    processes = LinuxFiles.get_process_tracker()
    for process in processes:
        name, pid = process.split(",")
        if name == "zcore-update-reboot":
            os.kill(int(pid), signal.SIGTERM)
    LinuxFiles.clear_process_tracker
    if message:
        send_message(message)
    else:
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
        
def stop_and_start(triggerBackup, stop):
    linux_services.core_service("stop")
    LinuxFiles.delete_map_sand() 

    if triggerBackup:
        backup.backup_handler()
        if config.dynamicLootEnabled:
            dynamic_loot()
        
            
    if not stop:
        linux_services.core_service("start")
        time.sleep(15)
        discord.discord_player_notifications("Server starting")

    linux_services.sys_calls("start", "zomboid_reboot.timer")


def restart_handler(message, delay, triggerBackup, stop):
    linux_services.sys_calls("stop", "zomboid_reboot.timer")
    try:
        ShutdownDelay = DelayCalculator(int(delay))
    except ValueError as verr:
            sys.exit(f"{verr}")
    except TypeError:
        ShutdownDelay = DelayCalculator()

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
            time.sleep(300)
            restart_handler("a restart and a 15 minute backup",
                None, True, False)
        elif sixHoursAfterStart < currentTime:
            restart_handler(None, None, False, False)
        else:
            lgsm.lgsm_passthrough("checkModsNeedUpdate")