import subprocess
from subprocess import CalledProcessError
from tools.linux_files import LinuxFiles as files

def add_user(name, password):
    if name and password:
        lgsm_passthrough([f"adduser \"{name}\" {password}"])

def ban_id(steam_id):
    if steam_id:
        lgsm_passthrough([f"banid {steam_id}"])

def unban_id(steam_id):
    if steam_id:
        lgsm_passthrough([f"unbanid {steam_id}"])

def kick_user(name):
    if name:
        lgsm_passthrough([f"kickuser {name}"])

def send_server_message(message):
    if message:
        lgsm_passthrough([f"servermsg \"{message}\""])

def save_server():
    lgsm_passthrough(["save-all"])

def add_item(name, item):
    if name:
        lgsm_passthrough([f"additem \"{name}\" {item}"])

def port_player(name, direction):
    if name:
        lgsm_passthrough([f"portplayer {direction} \"{name}\""])

def set_access_level(name, accessLevel):
    if name:
        lgsm_passthrough([f"setaccesslevel \"{name}\" {accessLevel}"])

def teleport_to(name, x, y, z):
    if name:
        lgsm_passthrough([f"teleportto \"{name}\" {x},{y},{z}"]) 

def lgsm_passthrough(command):
    try:
        result = subprocess.run([f"{files.pzlgsm}/pzserver", "send", command], check=True, text=True, capture_output=True)
        return result
    except CalledProcessError as e:
        print(f"{e}.")
        return None