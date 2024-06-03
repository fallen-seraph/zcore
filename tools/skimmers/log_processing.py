import time
from tools import restart
from tools import linux_services
from tools import discord

def debug_log(line):
    if "Mods need update" in line:
        restart.restart_handler("a mod update", None, False, False)
    elif "Failed to connect to Steam servers" in line:
        time.sleep(20)
        discord.discord_player_notifications("Steam connection failure, "
            "restarting.")
        active, activeTime = linux_services.get_service_info(
        "zomboid_core.service")
        active = active.split("=")[1]
        if active != "active":
            linux_services.core_service("restart")
        else:
            linux_services.core_service("start")
            
