from watchdog.events import FileSystemEventHandler

class DebugLogHandler(FileSystemEventHandler):
    def __init__(self, directory, line_processor, fileEndsWith):
        self.directory = directory
        self.fileEndsWith = fileEndsWith
        self.currentFile = None
        self.fileHandle = None
        self.line_processor = line_processor
        self.processList = []
        
    def on_modified(self, event):
        if event.is_directory:
            return
        self.log_handler(event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return
        self.log_handler(event.src_path)

    def log_handler(self, filepath):
        self.get_latest_updated_file(filepath)
        self.read_lines_from_latest_log()

    def get_latest_updated_file(self, filepath):
        if not filepath.endswith(self.fileEndsWith):
            return
        if self.currentFile is None or self.currentFile != filepath:
            self.currentFile = filepath
            if self.fileHandle:
                self.fileHandle.close()
            self.fileHandle = open(filepath, 'r')
            self.fileHandle.seek(0, 2)

    def read_lines_from_latest_log(self):
        while True:
            line = self.fileHandle.readline() # type: ignore
            if not line:
                break
            process = self.line_processor(line)
            self.join_processes()           
            if process:
                self.processList.append(process)

    def join_processes(self):
        for process in self.processList:
            if not process.is_alive():
                process.join()
                self.processList.remove(process)