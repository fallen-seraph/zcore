import json
from tools.linux_files import LinuxFiles as files

#for windows testing
json = json.load(open(fr"{__file__}\..\..\config.json"))
#json = json.load(open(f"{files.get_home()}/Server-Core/config.json"))
rcon_port = json['rcon_port']
rcon_password = json['rcon_password']
backupRetentionDays = json['backupRetentionDays']
discordNotifChnID = json['discordNotifChnID']

print("Configurations loaded.")