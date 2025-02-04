from disnake import SyncWebhook

from tools import (
    lgsm,
    messages,
    file_manager,
    linux_services
)

from utils.config import Configurations

config = Configurations()

def send_message(finalMessage):
    lgsm.send_server_message(finalMessage)
    discord_player_notifications(finalMessage)

def cancel_pending_restart(message):
    processTracking = file_manager.ZCoreFiles()
    processes = processTracking.get_process_tracker()

    if processes:
        linux_services.kill_restart_process(processes)
        processTracking.clear_process_tracker
    else:
        linux_services.sys_calls("stop", "zomboid_reboot.service")

    messageBuilder = messages.MessageHandler(message)

    if messageBuilder.message == "a scheduled reboot":    
        send_message("Restart Cancelled")
    else:
        send_message(messageBuilder.message)

def discord_player_notifications(message):
    if config.playerNotificationURL:
        try:
            SyncWebhook.from_url(config.playerNotificationURL).send(message)
        except Exception as e:
            print(e)

def discord_admin_notifications(message):
    if config.adminNotificationURL:
        try:
            SyncWebhook.from_url(config.adminNotificationURL).send(message)
        except Exception as e:
            print(e)