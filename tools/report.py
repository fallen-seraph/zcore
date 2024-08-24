from subprocess import run, PIPE, CalledProcessError

from tools import discord
from tools import fileManager

def crash_report():
    #Crash report generator
    discordMessage = "# The server is down."
    discord.discord_admin_notifications(discordMessage)

    try:
        diskReport = run(["df", "-h", "/"], stdout=PIPE, text=True).stdout
    except CalledProcessError as e:
        print(f"Disk Report failed: {e}")

    diskReport = "".join(["\n## Disk report output:\n", diskReport])

    discord.discord_admin_notifications(diskReport)

    try:
        journalReport = run(["journalctl", "--user", "-qn10"], stdout=PIPE,
            text=True).stdout
    except CalledProcessError as e:
        print(f"Disk Report failed: {e}")

    journalReport = "".join(["\n## journalctl log output:\n", journalReport])

    discord.discord_admin_notifications(journalReport)

    zcoreFiles = fileManager.ZCoreFiles()
    debugLogTail = zcoreFiles.latest_debug_log()

    debugLogTail = ''.join(debugLogTail)

    debugLogTail = "".join(["\n## Zomboid debug log output:\n", debugLogTail])

    discord.discord_admin_notifications(debugLogTail)