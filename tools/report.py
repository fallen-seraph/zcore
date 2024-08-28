from subprocess import run, PIPE, CalledProcessError

import file_manager
import utilities

def crash_report():
    #Crash report generator
    discordMessage = "# The server is down."
    utilities.discord_admin_notifications(discordMessage)

    try:
        diskReport = run(["df", "-h", "/"], stdout=PIPE, text=True).stdout
    except CalledProcessError as e:
        print(f"Disk Report failed: {e}")

    diskReport = "".join(["\n## Disk report output:\n", diskReport])

    utilities.discord_admin_notifications(diskReport)

    try:
        journalReport = run(["journalctl", "--user", "-qn10"], stdout=PIPE,
            text=True).stdout
    except CalledProcessError as e:
        print(f"Disk Report failed: {e}")

    journalReport = "".join(["\n## journalctl log output:\n", journalReport])

    utilities.discord_admin_notifications(journalReport)

    zcoreFiles = file_manager.ZCoreFiles()
    debugLogTail = zcoreFiles.latest_debug_log()

    debugLogTail = ''.join(debugLogTail)

    debugLogTail = "".join(["\n## Zomboid debug log output:\n", debugLogTail])

    utilities.discord_admin_notifications(debugLogTail)