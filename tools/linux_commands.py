from threading import Thread
import subprocess
from subprocess import CalledProcessError

def compress(backupPath, today, stagingPath):
    try:
        subprocess.run([
            "tar",
            "-czf",
            f"{backupPath}/{today}_backup.tar.gz",
            "-C", stagingPath,
            "."
        ])
    except CalledProcessError as e:
        print(f"An error occured: {e}.")

def start_compress_thread(backupPath, today, stagingPath):
    stagingPath = backupPath / "staging/"
    thread = Thread(target=compress, args=(backupPath, today, stagingPath))
    thread.start()
    return thread

def start_backup(backupPath, zomboidPath):
    try:
        stagingPath = backupPath / "staging/"
        subprocess.run(["rsync", "-aq", "--exclude", "backups",
            "--delete", f"{zomboidPath}/", stagingPath])
    except CalledProcessError as e:
        print(f"An error occured: {e}.")