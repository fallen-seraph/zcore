import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from tools.linux_files import LinuxFiles

from tools.skimmers import log_processing

class LogHandler(FileSystemEventHandler):
    def __init__(self, directory, process_line_callback):
        self.directory = directory
        self.process_line_callback = process_line_callback
        self.current_file = None
        self.file_handle = None

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
            self.process_line_callback(line)

def process_line(line):
    threading.Thread(target=log_processing.debug_log, args=(line,)).start()

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