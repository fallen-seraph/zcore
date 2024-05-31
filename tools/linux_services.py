from subprocess import run, PIPE, CalledProcessError
from tools.linux_files import LinuxFiles as lf
import sys

def SysCall(command, serviceFile):
    try:
        run(["systemctl", "--user", command, serviceFile])
    except CalledProcessError as e:
        print(f"An error occured: {e}.")

def StartAllServices():
    for file in lf.get_sysd_files():
        SysCall("start", file)

def MainServices(command):
    for file in ["zomboid_main.service", "zomboid_skimmer.service"]:
        SysCall(command, file)

def get_service_info(service_name):
    try:
        result = run(["systemctl", "show", service_name, "--property=ActiveEnterTimestamp,ActiveState"], stdout=PIPE, text=True)
        return result.stdout.strip().split("\n")
    except CalledProcessError as e:
        sys.exit(f"An error occured: {e}.")