from disnake import SyncWebhook
from utils import config

def discord_player_notifications(message):
    try:
        SyncWebhook.from_url(config.playerNotificationURL).send(message)
    except Exception as e:
        print(e)

def discord_admin_notifications(message):
    try:
        SyncWebhook.from_url(config.adminNotificationURL).send(message)
    except Exception as e:
        print(e)