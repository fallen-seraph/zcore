from configs.config import rcon_port, rcon_password
from rcon.source import Client
import socket

def Rcon(command):
    try:
        with Client("127.0.0.1", rcon_port, passwd=rcon_password, timeout=15) as client:
            return client.run(command)
    except socket.timeout as timeout:
        return timeout
    except ConnectionRefusedError as CRE:
        return(f"{CRE}\n Is the server offline?")