import subprocess
from subprocess import CalledProcessError
from tools.linux_files import LinuxFiles as files
import requests

def deploy_lgsm():
    pzlFolder, file = files.manage_lgsm_files()
    try:
        open(file, 'w').write(
            requests.get("https://linuxgsm.sh").text)
        
        subprocess.run(["bash", "linuxgsm.sh", "pzserver"], cwd=pzlFolder,
            check=True, text=True, shell=False, capture_output=True)

        subprocess.run([f"{pzlFolder}/pzserver", "install"], cwd=pzlFolder, input='Y\nY\nN\n',
            check=True, text=True, shell=False)

    except ConnectionError as e:
        print(f"Connection Error occured: {e}")
    except CalledProcessError as e:
        print(f"An error occured: {e}.")


def deploy_sysd():
    files.manage_sysd_files()

    try:
        subprocess.run(["loginctl", "enable-linger"], check=True, text=True,
            shell=False)
        
        subprocess.run(["systemctl", "--user", "daemon-reload"], check=True, text=True,
            shell=False)
        
        for x in files.get_sysd_files():
            subprocess.run(["systemctl", "--user", "enable", x], check=True,
                text=True, shell=False)
        
    except CalledProcessError as e:
        print(f"An error occured: {e}")

def misc_tasks():
    files.prep_backup_directories()
    files.prep_chunk_directory()
