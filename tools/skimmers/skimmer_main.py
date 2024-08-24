import time
from watchdog.observers import Observer

from tools.skimmers import debug_skimmer, log_processing
from tools import fileManager

def monitor_logs():
    zcoreFiles = fileManager.ZCoreFiles
    event_handler = debug_skimmer.DebugLogHandler(zcoreFiles.zomboidLogs,
        log_processing.debug_line_process, "_DebugLog-server.txt")
    observer = Observer()
    observer.schedule(event_handler, zcoreFiles.zomboidLogs, False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        observer.stop()
        zcoreFiles.clear_process_tracker()
    observer.join()