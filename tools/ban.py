import time
from tools.lgsm import ban_id

def console_ban_handler(file):
    with file as openFile:
        banList = openFile.readlines()

    for x in banList:
        x = x.strip()
        ban_id(x)
        print(f"Banning id: {x}")
        time.sleep(2)