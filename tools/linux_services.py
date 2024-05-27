from subprocess import run, CalledProcessError
from tools.linux_files import LinuxFiles as lf

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