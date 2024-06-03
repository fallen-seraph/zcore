import time
from tools import restart, linux_services, discord

def debug_log(line):
    if "Mods need update" in line:
        restart.restart_handler("a mod update", None, False, False)
    elif "Failed to connect to Steam servers" in line:
        time.sleep(20)
        discord.discord_player_notifications("Steam connection failure, "
            "restarting.")
        active = linux_services.get_service_status("zomboid_core.service")[1]
        if active != "active":
            linux_services.core_service("restart")
        else:
            linux_services.core_service("start")
            
