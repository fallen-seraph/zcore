import time
from watchdog.observers import Observer

from tools.linux_files import LinuxFiles
from tools.skimmers import debug_skimmer, log_processing

def monitor_logs():
    directory = LinuxFiles.get_zomboid_logs()
    event_handler = debug_skimmer.DebugLogHandler(directory,
        log_processing.debug_line_process, "_DebugLog-server.txt")
    observer = Observer()
    observer.schedule(event_handler, directory, False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        observer.stop()
        LinuxFiles.clear_process_tracker()
    observer.join()