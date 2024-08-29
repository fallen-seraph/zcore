import re
import time
from multiprocessing import Process
from watchdog.observers import Observer

from tools import (
    file_manager,
    restart,
    linux_services,
    utilities
)

from tools.skimmers import debug_skimmer
from tools.file_manager import ZCoreFiles

def read_from_latest_debug_log(logLine):
    if re.match(
        "^\[.*\] LOG  : General.*> CheckModsNeedUpdate: Mods need update\.$",
        logLine
    ):
        processName = "zcore-update-reboot"
        process = Process(
            target=restart.restart_server_with_messages,
            args=("a mod update"),
            name=processName
        )
        process.start()
        file_manager.ZCoreFiles().create_process_tracker(
            processName,
            process.pid
        )
        return process
    elif re.match(
        "^\[.*\] LOG  : General.*> Failed to connect to Steam servers.$",
        logLine
    ):
        process = Process(target=restart_if_steam_is_down, args=())
        process.start()
        return process
    
def restart_if_steam_is_down():
    time.sleep(20)
    utilities.discord_player_notifications(
        "Steam connection failure, restarting."
    )
    active = linux_services.get_service_status("zomboid_core.service")[1]
    if active == "active":
        linux_services.core_service("restart")
    else:
        linux_services.core_service("start")
    time.sleep(10)

def monitor_logs():
    zcoreFiles = ZCoreFiles()

    event_handler = debug_skimmer.DebugLogHandler(
        zcoreFiles.zomboidLogs,
        read_from_latest_debug_log(),
        "_DebugLog-server.txt"
    )

    observer = Observer()
    observer.schedule(event_handler, zcoreFiles.zomboidLogs, False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        observer.stop()
        zcoreFiles.clear_process_tracker()
        
    observer.join()