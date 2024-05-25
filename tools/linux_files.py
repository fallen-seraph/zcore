from subprocess import run, PIPE, CalledProcessError
from pathlib import Path,PurePosixPath
from requests import get
from shutil import copy2
from os import scandir

class linux_files:
    __home = Path.home()
    __systemctlPath = PurePosixPath(__home).joinpath(
        ".config/systemd/user")
    __rcon = PurePosixPath(__home).joinpath("rcon/rcon")
    __fullBackups = PurePosixPath(__home).joinpath("backups")
    __pzlgsm = PurePosixPath(__home).joinpath("pzlgsm")
    __zomboid = PurePosixPath(__home).joinpath("Zomboid/")
    __logs = PurePosixPath(__zomboid).joinpath("Logs")
    __save = PurePosixPath(__zomboid).joinpath(
        "Saves/Multiplayer/pzserver")
    __zomboidBackups = PurePosixPath(__zomboid).joinpath(
        "backups")
    __serverini = PurePosixPath(__zomboid).joinpath(
        "Server/pzserver.ini")
    __accountDB = PurePosixPath(__zomboid).joinpath(
        "db/pzserver.db")
        
    @classmethod
    def deploy_lgsm(self):
        Path(self.__pzlgsm).mkdir(exist_ok=True)

        file = self.__pzlgsm.joinpath("linuxgsm.sh")
        Path(file).touch(mode=0o700)

        open(file, 'w').write(
            get("https://linuxgsm.sh").text)
        try:
            result = run(["bash", "linuxgsm.sh", "pzserver"]
                        , cwd=self.__pzlgsm, check=True, text=True
                        , shell=False, capture_output=True)
            print(result)

            try:
                run([f"{self.__pzlgsm}/pzserver", "install"], input='Y\nY\nN\n'
                    , check=True, text=True, shell=False)
            except CalledProcessError as e:
                print(f"An error occured: {e}.")

        except CalledProcessError as e:
            print(f"An error occured: {e}.")

    @classmethod
    def create_sysd_folders(self):
        Path(self.__systemctlPath).mkdir(parents=True, exist_ok=True)

    @classmethod
    def deploy_sysd_files(self):
        path = PurePosixPath(f"{self.__home}/Server-Core/install/service-files")
        files = [x.name for x in scandir(path) if x.is_file()]

        for x in files:
            copy2(f"{path}/{x}", self.__systemctlPath)