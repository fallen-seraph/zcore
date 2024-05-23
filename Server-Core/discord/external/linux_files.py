from subprocess import run, PIPE, CalledProcessError
from pathlib import Path,PurePosixPath
from requests import get

class linux_files:
    def __init__(self):
        self.__home = Path.home()
        self.__systemctlPath = PurePosixPath(self.__home).joinpath(
            ".config/systemd/user")
        self.__rcon = PurePosixPath(self.__home).joinpath("rcon/rcon")
        self.__fullBackups = PurePosixPath(self.__home).joinpath("backups")
        self.__pzlgsm = PurePosixPath(self.__home).joinpath("pzlgsm")
        self.__zomboid = PurePosixPath(self.__home).joinpath("Zomboid/")
        self.__logs = PurePosixPath(self.__zomboid).joinpath("Logs")
        self.__save = PurePosixPath(self.__zomboid).joinpath(
            "Saves/Multiplayer/pzserver")
        self.__zomboidBackups = PurePosixPath(self.__zomboid).joinpath(
            "backups")
        self.__serverini = PurePosixPath(self.__zomboid).joinpath(
            "Server/pzserver.ini")
        self.__accountDB = PurePosixPath(self.__zomboid).joinpath(
            "db/pzserver.db")

    def create_lgsm_folder(self):
        Path(self.__pzlgsm).mkdir(exist_ok=True)

    def create_linuxgsm(self):
        file = self.__pzlgsm.joinpath("linuxgsm.sh")
        Path(file).touch(mode=0o700)

        try:
            open(file, 'w').write(
                get('https://linuxgsm.sh').text)
            try:
                result = run(["bash", "linuxgsm.sh", "pzserver"]
                             , cwd=self.__pzlgsm, check=True, text=True
                             , shell=False, capture_output=True)
                print(result)
            except CalledProcessError as e:
                print(f"An error occured: {e}.")
        except ConnectionError as e:
            print(f"An error occured: {e}.")

    def download_pzserver(self):
        try:
            run([f"{self.__pzlgsm}/pzserver", "install"], input='Y\nY\nN\n'
                , check=True, text=True, shell=False)
        except CalledProcessError as e:
            print(f"An error occured: {e}.")

    def create_sysd_folders(self):
        Path(self.__systemctlPath).mkdir(parents=True, exist_ok=True)