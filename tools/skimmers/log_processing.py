import time
from tools import restart, linux_services, discord

def mod_update():
    restart.restart_handler("a mod update", None, False, False)
    time.sleep(10)

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