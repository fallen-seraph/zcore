import json

print("Configurations loaded.")

json = json.load(open('../config.json'))
rcon_port = json['rcon_port']
rcon_password = json['rcon_password']
backupRetentionDays = json['']
discordNotifChnID = json['discordNotifChnID']