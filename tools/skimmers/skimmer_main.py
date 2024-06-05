import time
from watchdog.observers import Observer

from tools.linux_files import LinuxFiles
from tools.skimmers import debug_skimmer

def monitor_directory():
    directory = LinuxFiles.get_zomboid_logs()
    event_handler = debug_skimmer.LogHandler(directory)
    observer = Observer()
    observer.schedule(event_handler, directory, False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()