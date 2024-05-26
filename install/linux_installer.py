from subprocess import run, PIPE, CalledProcessError
from requests import get
from tools.linux_files import LinuxFiles as files

def DeployLgsm():
    pzlFolder, file = files.ManageLgsmFiles()
    try:
        open(file, 'w').write(
            get("https://linuxgsm.sh").text)
        
        run(["bash", "linuxgsm.sh", "pzserver"], cwd=pzlFolder,
            check=True, text=True, shell=False, capture_output=True)

        run([f"{pzlFolder}/pzserver", "install"], input='Y\nY\nN\n',
            check=True, text=True, shell=False)

    except ConnectionError as e:
        print(f"Connection Error occured: {e}")
    except CalledProcessError as e:
        print(f"An error occured: {e}.")


def DeploySysdFiles():
    sysFiles = files.ManageSysdFiles()
    try:
        run(["loginctl", "enable-linger"], check=True, text=True,
            shell=False)
        
        run(["systemctl", "--user", "daemon-reload"], check=True, text=True,
            shell=False)
        
        for x in sysFiles:
            run(["systemctl", "--user", "enable", x], check=True,
                text=True, shell=False)
        
    except CalledProcessError as e:
        print(f"An error occured: {e}")
