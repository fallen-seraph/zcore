import re
import time
from multiprocessing import Process

from tools import restart, linux_services, discord

from tools.linux_files import LinuxFiles

def debug_line_process(line):
    print(line)

    if re.match("^\[.*\] LOG  : General.*> CheckModsNeedUpdate: Mods need "
        "update\.$", line):
        processName = "zcore-update-reboot"
        process = Process(target=mod_update, args=(), name=processName)
        process.start()
        LinuxFiles.create_process_tracker(processName, process.pid)
        return process
    elif re.fullmatch("^\[.*\] LOG  : General.*> Failed to connect to Steam "
        "servers.$", line):
        process = Process(target=steam_down, args=())
        process.start()
        return process

def mod_update():
    linux_services.sys_calls("stop", "zomboid_reboot.timer")
    restart.restart_handler("a mod update", None, False, False)
    time.sleep(10)
    linux_services.sys_calls("start", "zomboid_reboot.timer")

def steam_down():
    print("Steam's down")
    time.sleep(20)
    discord.discord_player_notifications("Steam connection failure, "
        "restarting.")
    active = linux_services.get_service_status("zomboid_core.service")[1]
    if active != "active":
        linux_services.core_service("restart")
    else:
        linux_services.core_service("start")
    time.sleep(10)