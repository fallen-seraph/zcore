from tools.file_manager import ZomboidConfigurationFiles, GlobalZomboidBackups
from tools import (
    linux_commands,
    scheduler
)

def backup_handler():
    globalBackupFiles = GlobalZomboidBackups()
    backupPath = globalBackupFiles.dailyBackups
    stagingPath = backupPath / "staging/"
    ZomboidConfigurationFiles().update_hours_for_loot_respawn()

    today = scheduler.truncate_date_as_string()

    linux_commands.start_backup(
        backupPath,
        stagingPath,
        globalBackupFiles.zomboidPath,
    )

    thread = linux_commands.start_compress_thread(
        backupPath,
        today,
        stagingPath,
    )
    
    globalBackupFiles.remove_oldest_backup(
        scheduler.get_date_of_backup_period_start()
    )

    return thread