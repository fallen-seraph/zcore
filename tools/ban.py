import time
from tools import lgsm

def console_ban_handler(file):
    with file as openFile:
        banList = openFile.readlines()

    for x in banList:
        x = x.strip()
        lgsm.ban_id(x)
        print(f"Banning id: {x}")
        time.sleep(2)