from subprocess import run, PIPE, CalledProcessError
from tools import discord

def crash_report():
    #Crash report generator
    discordMessage = "The server is down."
    discord.discord_admin_notifications(discordMessage)

    try:
        diskReport = run(["df", "-h", "/"], stdout=PIPE, text=True).stdout
    except CalledProcessError as e:
        print(f"Disk Report failed: {e}")

    discord.discord_admin_notifications(diskReport)

    try:
        journalReport = run(["journalctl", "--user", "-qn20"], stdout=PIPE,
            text=True).stdout
    except CalledProcessError as e:
        print(f"Disk Report failed: {e}")

    discord.discord_admin_notifications(journalReport)