import re
import time
from multiprocessing import Process

from tools import file_manager, restart, linux_services, utilities

def debug_line_process(line):
    if re.match("^\[.*\] LOG  : General.*> CheckModsNeedUpdate: Mods need "
        "update\.$", line):
        processName = "zcore-update-reboot"
        process = Process(target=restart.restart_server_with_messages, args=(
            "a mod update"), name=processName)
        process.start()
        file_manager.ZCoreFiles().create_process_tracker(
            processName,
            process.pid
        )
        return process
    elif re.match("^\[.*\] LOG  : General.*> Failed to connect to Steam "
        "servers.$", line):
        process = Process(target=steam_down, args=())
        process.start()
        return process

def steam_down():
    time.sleep(20)
    utilities.discord_player_notifications("Steam connection failure, "
        "restarting.")
    active = linux_services.get_service_status("zomboid_core.service")[1]
    if active != "active":
        linux_services.core_service("restart")
    else:
        linux_services.core_service("start")
    time.sleep(10)