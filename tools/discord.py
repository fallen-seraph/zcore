from disnake import SyncWebhook
from utils import config

def discord_player_notifications(message):
    SyncWebhook.from_url(config.playerNotificationURL).send(message)

def discord_admin_notifications(message):
    SyncWebhook.from_url(config.adminNotificationURL).send(message)