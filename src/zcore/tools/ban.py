import time
from tools.lgsm import ban_id

def console_ban_handler(file):
    with file as openFile:
        banList = openFile.readlines()

    for steamID in banList:
        steamID = steamID.strip()
        ban_id(steamID)
        print(f"Banning id: {steamID}")
        time.sleep(2)