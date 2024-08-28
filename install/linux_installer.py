import requests
import subprocess
from subprocess import CalledProcessError
from tools import file_manager

class Installer():
    def __init__(self):
        self.linuxFiles = file_manager.LinuxFileSystem()

    def deploy_lgsm(self):
        lgsmFiles = file_manager.LGSMFiles()
        lgsmFiles.create_pzlgsm_directory()
        pzlFolder, file = lgsmFiles.create_lgsm_file()
        try:
            open(file, 'w').write(
                requests.get("https://linuxgsm.sh").text)
            
            subprocess.run(["bash", "linuxgsm.sh", "pzserver"], cwd=pzlFolder,
                check=True, text=True, shell=False, capture_output=True)

            subprocess.run([f"{pzlFolder}/pzserver", "install"], cwd=pzlFolder,
                input='Y\nY\nN\n', check=True, text=True, shell=False)
            
            lgsmFiles.default_server_password()

        except ConnectionError as e:
            print(f"Connection Error occured: {e}")
        except CalledProcessError as e:
            print(f"An error occured: {e}.")


    def deploy_sysd(self):
        self.linuxFiles.copy_packaged_sysd_files()

        try:
            subprocess.run(["loginctl", "enable-linger"], check=True, text=True,
                shell=False)
            
            subprocess.run(["systemctl", "--user", "daemon-reload"], check=True,
                text=True, shell=False)
            
            for x in self.linuxFiles.get_sysd_files():
                subprocess.run(["systemctl", "--user", "enable", x], check=True,
                    text=True, shell=False)
            
        except CalledProcessError as e:
            print(f"An error occured: {e}")

    def misc_tasks(self):
        zBackups = file_manager.GlobalZomboidBackups()
        zBackups.create_backup_directories()
        zomboidChunks = file_manager.ZomboidChunks()
        zomboidChunks.prep_chunk_directory()
        
        self.linuxFiles.alias_creation()