from configs import apaconfig
from subprocess import run, PIPE, CalledProcessError

class apa_rcon:
    def __init__(self, IP=apaconfig.local_IP, port=apaconfig.local_port, password=apaconfig.local_password):
        self._IP = IP
        self._port = port
        self._password = password

    def rcon_execute(self, command):
        try:
            result = run(["rcon", "-a", self._IP + self._port, "-p", self._password, command], stdout=PIPE, check=True, text=True, shell=False, capture_output=True)
            return result.stdout
        except CalledProcessError as e:
            print(f"Unable to rcon: {e}.")
            return None