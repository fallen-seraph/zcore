from subprocess import run, PIPE, CalledProcessError
from requests import get
from tools.linux_files import LinuxFiles as lf

def DeployLgsm():
    pzlFolder, file = lf.ManageLgsmFiles()
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
    files = lf.ManageSysdFiles()
    try:
        run(["loginctl", "enable-linger"], check=True, text=True,
            shell=False)
        
        run(["systemctl", "--user", "reload-daemon"], check=True, text=True,
            shell=False)
        
        for x in files:
            run(["systemctl", "--user", "enable", x], check=True,
                text=True, shell=False)
        
    except CalledProcessError as e:
        print(f"An error occured: {e}")