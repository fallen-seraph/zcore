import tools.linux_services as services
import tools.tools_lgsm as lgsm
import tools.tools_timer as tools_timer
import tools.tools_backup as tools_backup
from tools.linux_files import LinuxFiles as files
from config import dynamicLootEnabled, dynamicLootRange, dailyBackupTime, dailyBackupTimeZone
from datetime import datetime, timedelta
import pytz
import random
import time
import sys
import re

def send_message(fullMessage):
    lgsm.send_server_message(fullMessage)

def instant_restart():
    services.main_services("restart")

def stop_and_start(backup, stop):
    services.main_services("stop")     

    if backup:
        tools_backup.backup_handler()

    #map_sand.bin
    #aggregated.log

    if not stop:
        services.main_services("start")

def cancel_restart():
    services.sys_calls("stop", "zomboid_reboot.service")
    send_message("Reboot cancelled")

def dynamic_loot():
    low, high = dynamicLootRange.split(",")
    random.randrange(low, high)
    iniFile = files.open_ini_file()
    oldValue = re.search("HoursForLootRespawn=.*", iniFile)
    if oldValue:
        newContents = iniFile.replace(oldValue.group(0), "HoursForLootRespawn=10")
        files.write_ini_file(newContents)

def restart_handler(message, delay, backup, stop):
    try:
        ShutdownDelay = tools_timer.DelayCalculator(int(delay))
    except ValueError as verr:
            sys.exit(f"{verr}")
    except TypeError:
        ShutdownDelay = tools_timer.DelayCalculator()

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

    stop_and_start(backup, stop)

def restart_schedular():
    active, activeTime = services.get_service_info("zomboid_core.service")
    active = active.split("=")[1]
    
    if active == "active":
        backupHour, backupMinute = dailyBackupTime.split(":")

        if not dailyBackupTimeZone == "UTC":
            backupTimeZone = pytz.timezone(dailyBackupTimeZone)
            backupTime = datetime.now(backupTimeZone).replace(hour=int(
                backupHour), minute=int(backupMinute)).astimezone(pytz.utc)
        else:
            backupTime = datetime.now(pytz.utc).replace(hour=int(backupHour), 
                minute=int(backupMinute))
        
        currentTime = datetime.now(pytz.utc)
        activeTime = activeTime.split("=")[1]
        activeTime = datetime.strptime(activeTime,
            "%a %Y-%m-%d %H:%M:%S %Z").astimezone(pytz.utc)
        sixHoursAgo = currentTime - timedelta(hours=6)

        if currentTime.strftime("%H:%M") == backupTime.strftime("%H:%M"):
            restart_handler("a restart and a 15 minute backup",
                None, True, False)
            if dynamicLootEnabled:
                dynamic_loot() 
        elif activeTime > sixHoursAgo:
            restart_handler(None, None, False, False)
        else:
            lgsm.lgsm_passthrough("checkModsNeedUpdate")