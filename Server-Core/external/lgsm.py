from subprocess import run, PIPE, check_output, CalledProcessError

class lgsm_commands:
    def __init__(self, name=None, password=None, steam_id=None, message=None, item=None):
        self._name = name
        self._password = password
        self._steam_id = steam_id
        self._message = message
        self._item = item

    def add_user(self):
        if self._name and self._password:
            self.execute([f"adduser \"{self._name}\" {self._password}"])
    
    def ban_id(self):
        if self._steam_id:
            self.execute([f"banid {self._steam_id}"])
    
    def unban_id(self):
        if self._steam_id:
            self.execute([f"unbanid {self._steam_id}"])

    def kick_user(self):
        if self._name:
            self.execute([f"kickuser {self._name}"])

    def send_server_message(self):
        if self._message:
            self.execute([f"servermsg \"{self._message}\""])

    def save_server(self):
        self.execute(["save-all"])

    def reward_participating_players(self):
        if self._name:
            self.execute([f"additem \"{self._name}\" {self._item}"])

    def port_player(self, direction):
        if self._name:
            self.execute([f"portplayer {direction} \"{self._name}\""])

    def set_access_level(self, accessLevel):
        if self._name:
            self.execute([f"setaccesslevel \"{self._name}\" {accessLevel}"])

    def teleport_to(self, x, y, z):
        if self._name:
            self.execute([f"teleportto \"{self._name}\" {x},{y},{z}"]) 

    def lgsm_execute(self, command):
        try:
            result = run(["pzserver", "send", command], stdout=PIPE, check=True, text=True, shell=False, capture_output=True)
            return result.stdout
        except CalledProcessError as e:
            print(f"Unable to send command: {e}.")
            return None