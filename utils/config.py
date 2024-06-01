import json
from tools.linux_files import LinuxFiles

#for windows testing
#json = json.load(open(fr"{__file__}\..\..\config.json"))
json = json.load(open(f"{LinuxFiles.get_home()}/zcore/config.json"))
rcon_port = json['rcon_port']
rcon_password = json['rcon_password']
backupRetentionDays = json['backupRetentionDays']
dailyBackupTime = json['dailyBackupTime']
dailyBackupTimeZone = json['dailyBackupTimeZone']
dynamicLootEnabled = json['dynamicLootEnabled']
dynamicLootRange = json['dynamicLootRange']
discordNotifChnID = json['discordNotifChnID']
serverDownNotifChnID = json['serverDownNotifChnID']
