import time

from tools import fileManager, linux_services, lgsm, backup, delay, messages, utilities

def restart_server_with_messages(message=None, providedDelay=None, triggerBackup=False, stop=False):
    delayCalc = delay.DelayCalculator(providedDelay)
    messageBuilder = messages.MessageHandler(message)

    linux_services.sys_calls("stop", "zomboid_reboot.timer")

    utilities.send_message(
        messageBuilder.reboot_time_message(
            delayCalc.getTargetTime()
        )
    )

    for interval in delayCalc.get_all_intervals():
        if not interval == 1:
            utilities.send_message(
                messageBuilder.interval_message(interval)
            )
            time.sleep(300)
        else:
            utilities.send_message(
                messageBuilder.one_minute_message()
            )
            time.sleep(30)

    lgsm.save_server()
    
    time.sleep(30)

    linux_services.core_service("stop")
    
    fileManager.MiscFileFunctions().delete_map_sand()

    thread = None

    if triggerBackup:
        thread = backup.backup_handler(True)
            
    if not stop:
        linux_services.core_service("start")
        time.sleep(15)
        linux_services.sys_calls("start", "zomboid_reboot.timer")

    if thread:
        thread.join()