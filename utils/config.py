import pytz
import configparser
from datetime import datetime
from tools import file_manager

class Configurations:
    def __init__(self):
        self.cparser = configparser.ConfigParser()
        self.cparser.read(file_manager.CoreFiles()._home / "zcore/config.ini")

        try:
            self.activeHoursBeforeRestart = self.cparser.getint(
                "RESTART",
                "activeHoursBeforeRestart"
            )
            self.backupRetentionDays = self.cparser.getint(
                "BACKUPS",
                "backupRetentionDays"
            )
            self.dailyBackupTime = self.validate_time(
                self.cparser.get(
                    "BACKUPS",
                    "dailyBackupTime"
                )
            )
            self.dailyBackupTimeZone = self.validate_time_zone(
                self.cparser.get(
                    "BACKUPS",
                    "dailyBackupTimeZone"
                )
            )
            self.dynamicLootEnabled = self.cparser.getboolean("DYNAMIC.LOOT", "dynamicLootEnabled")
            self.dynamicLootRange = self.validate_range(self.cparser.get("DYNAMIC.LOOT", "dynamicLootRange"))
            self.playerNotificationURL = self.cparser.get("DISCORD", "playerNotificationURL")
            self.adminNotificationURL = self.cparser.get("DISCORD", "adminNotificationURL")
        except (configparser.Error, ValueError) as e:
            print(f"Configuration error: {e}")

    def validate_time(self, value):
        try:
            datetime.strptime(value, "%H:%M")
            return value
        except ValueError:
            raise ValueError(f"Invalid time format: {value}")

    def validate_time_zone(self, value):
        if value not in pytz.all_timezones:
            raise ValueError(f"Invalid time zone: {value}")
        return value

    def validate_range(self, value):
        try:
            low, high = map(int, value.split("-"))
            if low > high:
                raise ValueError
            return (low, high)
        except ValueError:
            raise ValueError(f"Invalid range format: {value}")