from subprocess import run, PIPE, CalledProcessError
from tools.linux_files import LinuxFiles as lf

def SysCall(command, serviceFile):
    try:
        run(["systemctl", "--user", command, serviceFile])
    except CalledProcessError as e:
        print(f"An error occured: {e}.")

def StartAllServices():
    for file in lf.getSysdFiles():
        SysCall("start", file)
        

def RestartServices():
    for file in ["zomboid_main.service", "zomboid_skimmer.service"]:
        SysCall("restart", file)

def StopServices():
    for file in ["zomboid_main.service", "zomboid_skimmer.service"]:
        SysCall("stop", file)