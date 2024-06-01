import re

from tools import lgsm, restart

def debug_log(line):
    if "Mods need update" in line:
        restart.restart_handler("a mod update", None, False, False)