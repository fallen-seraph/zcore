import os
import re
import sys
import time
import pytz
import random
import signal
from datetime import datetime, timedelta

from tools import fileManager, linux_services, lgsm, backup, discord
from tools.delay import DelayCalculator

from utils import config


def send_message(fullMessage):
    lgsm.send_server_message(fullMessage)
    discord.discord_player_notifications(fullMessage)

def instant_restart():
    linux_services.core_service("restart")

def cancel_pending_restart(message):
    processTracking = fileManager.ZCoreFiles()
    if not message:
        message="Reboot Cancelled"
    processes = processTracking.get_process_tracker()
    if processes:
        for process in processes:
            name, pid = process.split(",")
            if name == "zcore-update-reboot":
                os.kill(int(pid), signal.SIGTERM)
        processTracking.clear_process_tracker
    else:
        linux_services.sys_calls("stop", "zomboid_reboot.service")
        
    send_message(message)

def dynamic_loot():
    zomboidConfigFiles = fileManager.ZomboidConfigurationFiles()
    low, high = config.dynamicLootRange
    newLootHours = random.randrange(low, high)
    iniFile = zomboidConfigFiles.open_ini_file()
    oldValue = re.search("HoursForLootRespawn=.*", iniFile)
    if oldValue:
        newContents = iniFile.replace(oldValue.group(0),
            f"HoursForLootRespawn={newLootHours}")
        zomboidConfigFiles.write_ini_file(newContents)

def restart_handler(message, delay, triggerBackup, stop):
    if not message:
        message="a scheduled reboot"
        
    baseMessage = f"Restarting the server for {message}"

    linux_services.sys_calls("stop", "zomboid_reboot.timer")
    
    try:
        ShutdownDelay = DelayCalculator(int(delay))
    except ValueError as verr:
            sys.exit(f"{verr}")
    except TypeError:
        ShutdownDelay = DelayCalculator()

    targetRebootTime = ShutdownDelay.getTargetTime()

    targetTimeMessage = " ".join([baseMessage, "at",
        f"<t:{targetRebootTime}:t>"])

    discord.discord_player_notifications(targetTimeMessage)

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

    linux_services.core_service("stop")
    
    miscFileFunctions = fileManager.MiscFileFunctions()
    miscFileFunctions.delete_map_sand()

    if triggerBackup:
        thread = backup.backup_handler(True)
        if config.dynamicLootEnabled:
            dynamic_loot()
                
    if not stop:
        linux_services.core_service("start")
        time.sleep(15)
        linux_services.sys_calls("start", "zomboid_reboot.timer")

    thread.join()

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