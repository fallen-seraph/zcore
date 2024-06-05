from multiprocessing import Process

from watchdog.events import FileSystemEventHandler

from tools.skimmers import log_processing

class LogHandler(FileSystemEventHandler):
    def __init__(self, directory):
        self.directory = directory
        self.currentFile = None
        self.fileHandle = None
        self.modUpdateThread = None

    def on_modified(self, event):
        if event.is_directory:
            return
        self.handle_file(event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return
        self.handle_file(event.src_path)

    def process_line(self, line):
        print("prematch: " + line)

        if "Mods need update" in line:
            if self.modUpdateThread is None or not self.modUpdateThread.is_alive():
                self.modUpdateThread = Process(target=log_processing.mod_update, args=(), name="zcore-update-reboot")
                self.modUpdateThread.start()
        elif "Failed to connect to Steam servers" in line:
            print("steam_down")
            #threading.Thread(target=log_processing.steam_down, args=()).start()

    def handle_file(self, filepath):
        if not filepath.endswith("_DebugLog-server.txt"):
            return
        if self.currentFile is None or self.currentFile != filepath:
            self.currentFile = filepath
            if self.fileHandle:
                self.fileHandle.close()
            self.fileHandle = open(filepath, 'r')
            self.fileHandle.seek(0, 2)

        while True:
            line = self.fileHandle.readline() # type: ignore
            if not line:
                break
            self.process_line(line)