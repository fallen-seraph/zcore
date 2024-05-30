from tools.linux_files import LinuxFiles as files
import tools.linux_services as services
import tools.tools_lgsm as lgsm
import tools.tools_timer as tools_timer
import tools.tools_backup as tools_backup
from configs.config import dynamicLootEnabled, dynamicLootRange
import random
import time
import sys
import re

def send_message(fullMessage):
    lgsm.send_server_message(fullMessage)

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

    services.MainServices("stop")

    if dynamicLootEnabled:
        dynamic_loot()        

    if backup:
        tools_backup.backup_handler()

    if not stop:
        services.MainServices("start")

def restart_schedular():
    print("time")