import sys
from subprocess import run, PIPE, CalledProcessError


def sys_calls(command, serviceFile):
    try:
        run(["systemctl", "--user", command, serviceFile])
    except CalledProcessError as e:
        print(f"An error occured: {e}.")

def core_service(command):
    sys_calls(command, "zomboid_core.service")

def get_service_status(service_name):
    try:
        result = run(["systemctl", "--user", "show", service_name,
            "--property=ActiveState"], stdout=PIPE, text=True)
        return result.stdout.strip().split("=")
    except CalledProcessError as e:
        sys.exit(f"An error occured: {e}.")

def get_service_info(service_name):
    try:
        result = run(["systemctl", "--user", "show", service_name, 
            "--property=ActiveEnterTimestamp,ActiveState"],
            stdout=PIPE, text=True)
        return result.stdout.strip().split("\n")
    except CalledProcessError as e:
        sys.exit(f"An error occured: {e}.")