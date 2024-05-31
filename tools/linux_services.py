from subprocess import run, PIPE, CalledProcessError
from tools.linux_files import LinuxFiles as lf
import sys

def sys_calls(command, serviceFile):
    try:
        run(["systemctl", "--user", command, serviceFile])
    except CalledProcessError as e:
        print(f"An error occured: {e}.")

def start_all_services():
    for file in lf.get_sysd_files():
        sys_calls("start", file)

def main_services(command):
    for file in ["zomboid_core.service", "zomboid_skimmer.service"]:
        sys_calls(command, file)

def get_service_info(service_name):
    try:
        result = run(["systemctl", "show", service_name, "--property=ActiveEnterTimestamp,ActiveState"], stdout=PIPE, text=True)
        return result.stdout.strip().split("\n")
    except CalledProcessError as e:
        sys.exit(f"An error occured: {e}.")