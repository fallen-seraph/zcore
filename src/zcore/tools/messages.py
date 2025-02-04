class MessageHandler:
    def __init__(self, message):
        self.message = self.default_message(message)
        self.baseMessage = f"Restarting the server for {self.message}"

    def default_message(self, message):
        if not message:
            message = "a scheduled reboot"
        return message

    def reboot_time_message(self, targetRebootTime):
        return " ".join([self.baseMessage, "at", f"<t:{targetRebootTime}:t>"])
    
    def interval_message(self, interval):
        return " ".join([self.baseMessage, f"in {interval} minutes."])

    def one_minute_message(self):
        return " ".join([self.baseMessage, "in 1 minute."])
    
