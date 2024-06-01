from tools import lgsm

def ban_handler(file):
    with open(file, "r") as openFile:
        banList = openFile.readlines() 

    for x in banList:
        lgsm.ban_id(x)