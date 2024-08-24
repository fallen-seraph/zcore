import re
import time
from multiprocessing import Process

from tools import fileManager, restart, linux_services, discord

def debug_line_process(line):
    if re.match("^\[.*\] LOG  : General.*> CheckModsNeedUpdate: Mods need "
        "update\.$", line):
        processName = "zcore-update-reboot"
        process = Process(target=restart.restart_handler, args=(
            "a mod update", None, False, False), name=processName)
        process.start()
        processFiles = fileManager.ZCoreFiles()
        processFiles.create_process_tracker(processName, process.pid)
        return process
    elif re.match("^\[.*\] LOG  : General.*> Failed to connect to Steam "
        "servers.$", line):
        process = Process(target=steam_down, args=())
        process.start()
        return process

def steam_down():
    time.sleep(20)
    discord.discord_player_notifications("Steam connection failure, "
        "restarting.")
    active = linux_services.get_service_status("zomboid_core.service")[1]
    if active != "active":
        linux_services.core_service("restart")
    else:
        linux_services.core_service("start")
    time.sleep(10)