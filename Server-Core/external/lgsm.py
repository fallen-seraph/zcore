from subprocess import run, PIPE, check_output, CalledProcessError

class lgsm_commands:
    def __init__(self, name=None, password=None, steam_id=None, message=None, item=None):
        self.name = name
        self.password = password
        self.steam_id = steam_id
        self.message = message
        self.item = item

    def add_user(self):
        if self.name and self.password:
            self.execute([f"adduser \"{self.name}\" {self.password}"])
    
    def ban_id(self):
        if self.steam_id:
            self.execute([f"banid {self.steam_id}"])
    
    def unban_id(self):
        if self.steam_id:
            self.execute([f"unbanid {self.steam_id}"])

    def kick_user(self):
        if self.name:
            self.execute([f"kickuser {self.name}"])

    def send_server_message(self):
        if self.message:
            self.execute([f"servermsg \"{self.message}\""])

    def save_server(self):
        self.execute(["save-all"])

    def reward_participating_players(self):
        if self.name:
            self.execute([f"additem \"{self.name}\" {self.item}"])

    def port_player(self, direction):
        if self.name:
            self.execute([f"portplayer {direction} \"{self.name}\""])

    def set_access_level(self, accessLevel):
        if self.name:
            self.execute([f"setaccesslevel \"{self.name}\" {accessLevel}"])

    def teleport_to(self, x, y, z):
        if self.name:
            self.execute([f"teleportto \"{self.name}\" {x},{y},{z}"]) 

    def lgsm_execute(self, command):
        try:
            result = run(["pzserver", "send", command], stdout=PIPE, check=True, text=True, shell=False, capture_output=True)
            return result.stdout
        except CalledProcessError as e:
            print(f"Unable to send command: {e}.")
            return None