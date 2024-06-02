import re
from datetime import datetime
import pytz
import configparser
from tools.linux_files import LinuxFiles

def validate_time(value):
    try:
        datetime.strptime(value, '%H:%M')
        return value
    except ValueError:
        raise ValueError(f"Invalid time format: {value}")

def validate_time_zone(value):
    if value not in pytz.all_timezones:
        raise ValueError(f"Invalid time zone: {value}")
    return value

def validate_range(value):
    try:
        low, high = map(int, value.split('-'))
        if low > high:
            raise ValueError
        return (low, high)
    except ValueError:
        raise ValueError(f"Invalid range format: {value}")


cparser = configparser.ConfigParser()
cparser.read(f"{LinuxFiles.get_home()}/zcore/config.ini")

try:
    backupRetentionDays = cparser.getint('BACKUPS', 'backupRetentionDays', )
    dailyBackupTime = validate_time(cparser.get('BACKUPS', 'dailyBackupTime'))
    dailyBackupTimeZone = validate_time_zone(cparser.get('BACKUPS', 'dailyBackupTimeZone'))

    dynamicLootEnabled = cparser.getboolean('DYNAMIC.LOOT', 'dynamicLootEnabled')
    dynamicLootRange = validate_range(cparser.get('DYNAMIC.LOOT', 'dynamicLootRange'))

    playerNotificationURL = cparser.get('DISCORD', 'playerNotificationURL')
    adminNotificationURL = cparser.get('DISCORD', 'adminNotificationURL')

    print("All configuration values are valid.")
except (configparser.Error, ValueError) as e:
    print(f"Configuration error: {e}")