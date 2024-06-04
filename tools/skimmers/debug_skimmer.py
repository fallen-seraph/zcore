import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from tools import restart, linux_services, discord, lgsm

from tools.linux_files import LinuxFiles

class LogHandler(FileSystemEventHandler):
    def __init__(self, directory, process_line_callback):
        self.directory = directory
        self.process_line_callback = process_line_callback
        self.current_file = None
        self.file_handle = None
        self.lock = threading.Lock()

    def on_modified(self, event):
        if event.is_directory:
            return
        self.handle_file(event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return
        self.handle_file(event.src_path)

    def handle_file(self, filepath):
        if not filepath.endswith("_DebugLog-server.txt"):
            return
        if self.current_file is None or self.current_file != filepath:
            self.current_file = filepath
            if self.file_handle:
                self.file_handle.close()
            self.file_handle = open(filepath, 'r')
            self.file_handle.seek(0, 2)

        while True:
            line = self.file_handle.readline() # type: ignore
            if not line:
                break
            self.process_line_callback(line, self.lock)

def process_line(line, lock):
    print("prematch: " + line)
    match line.split(","):
        case [*_, "Mods need update"]:
            lock.acquire()
            threading.Thread(target=restart.restart_handler, args=("a mod update", None, False, False)).start()
            time.sleep(10)
            lock.release()
        case [*_, "Failed to connect to Steam servers"]:
            print("Steam's down")
            time.sleep(20)
            discord.discord_player_notifications("Steam connection failure, "
                "restarting.")
            active = linux_services.get_service_status("zomboid_core.service")[1]
            lock.acquire()
            if active != "active":
                threading.Thread(target=linux_services.core_service, args=("restart",)).start()
            else:
                threading.Thread(target=linux_services.core_service, args=("start",)).start()
            time.sleep(10)
            lock.release()
    

def monitor_directory():
    directory = LinuxFiles.get_zomboid_logs()
    event_handler = LogHandler(directory, process_line)
    observer = Observer()
    observer.schedule(event_handler, directory, False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()