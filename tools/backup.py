from tools.file_manager import ZomboidConfigurationFiles, GlobalZomboidBackups
from tools import (
    linux_commands,
    scheduler
)

def backup_handler():
    globalBackupFiles = GlobalZomboidBackups()
    backupPath = globalBackupFiles.dailyBackups
    ZomboidConfigurationFiles().update_hours_for_loot_respawn()

    today = scheduler.truncate_date_as_string()
    nDaysAgo = scheduler.get_date_of_backup_period_start

    linux_commands.start_backup(
        backupPath,
        globalBackupFiles.zomboidPath,
        today
    )

    thread = linux_commands.start_compress_thread(
        backupPath,
        today
    )

    globalBackupFiles.remove_oldest_backup(nDaysAgo)

    return thread