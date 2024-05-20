import asyncio
#import config
import math
import re
import subprocess
from subprocess import check_output, CalledProcessError

RCON_COMMAND = ["rcon", "-a", "127.0.0.1:" + config.rcon_port, "-p", config.rcon_password]

#======================================================================================================================
def execute_adduser(name,password):

    zomboidCommand = [f"adduser \"{name}\" {password}"]
    return execute_command(RCON_COMMAND + zomboidCommand, f"Adding user name={name}")

#======================================================================================================================
def execute_banid(steam_id):

    zomboidCommand = [f"banid {steam_id}"]
    return execute_command(RCON_COMMAND + zomboidCommand, f"Banning steam ID={steam_id}")

#======================================================================================================================
def execute_unbanid(steam_id):

    zomboidCommand = [f"unbanid {steam_id}"]
    return execute_command(RCON_COMMAND + zomboidCommand, f"Unbanning steam ID={steam_id}")

#======================================================================================================================
def execute_pzkick(user):

    zomboidCommand = [f"kickuser {user}"]
    return execute_command(RCON_COMMAND + zomboidCommand, f"Kicking user={user}")

#======================================================================================================================
async def execute_sendMessage(message, bot):

    channel = bot.get_channel(1116144081987448893)

    await channel.send(message)

    try:
        p = subprocess.Popen(["pzserver", "send", f"servermsg \"{message}\""], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, errors = p.communicate()
    except CalledProcessError:
        print(f"{errors}")

    print(f"{output}")

#======================================================================================================================
def execute_restart():
    try:
        p = subprocess.Popen(["systemctl", "--user", "restart", "apathabove"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, errors = p.communicate()
    except CalledProcessError:
        print(f"{errors}")

    print(f"{output}")

#======================================================================================================================
def execute_save():
    try:
        p = subprocess.Popen(["pzserver", "send", "save-all"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, errors = p.communicate()
    except CalledProcessError:
        print(f"{errors}")

    print(f"{output}")

#======================================================================================================================
def execute_pzplayers():

    print("Retrieving online players...")
    try:
        pgrep_output = subprocess.run(RCON_COMMAND + ["players"], stdout=subprocess.PIPE, check=True, text=True).stdout
        players = pgrep_output.split("\n")
        return [player[1:] for player in players[1:] if len(player) > 0]

    except CalledProcessError:
        print("Error while executing 'rcon'")

    return "Error using RCON"

#======================================================================================================================
async def execute_pzrestart(message, timeTill, bot):
    print(f"Restarting the server in {timeTill} with message: \"{message}\"")

    timeTill = int(timeTill)

    if (timeTill != 0):
        interval = math.ceil(timeTill/3)
        loopCounter = 0

        while(loopCounter < 3):
            await execute_sendMessage(f"Restarting the server for {message} in {timeTill} minute(s).", bot)
            timeTill = timeTill - interval
            loopCounter += 1
            await asyncio.sleep(interval*60)

        execute_save()

        await asyncio.sleep(30)

        execute_restart()
    else:
        execute_save()

        await asyncio.sleep(30)
    
        execute_restart()
    
#======================================================================================================================
def execute_command(command,output):
    print(output)
    try:
        pgrep_output = subprocess.run(command, stdout=subprocess.PIPE, check=True, text=True).stdout
        return re.sub('password.*',"password provided",pgrep_output.strip())
    except CalledProcessError:
        print("Error while executing 'rcon'")

    return "Error using RCON"