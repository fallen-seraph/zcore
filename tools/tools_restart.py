import tools.linux_services as services
import tools.tools_lgsm as lgsm
import tools.timer as timer
import tools.tools_backup as tools_backup
import time
import sys

def send_message(fullMessage):
    lgsm.send_server_message(fullMessage)


def main(message, delay, backup):
    try:
        ShutdownDelay = timer.DelayCalculator(int(delay))
    except ValueError as verr:
            sys.exit(f"{verr}")
    except IndexError:
        ShutdownDelay = timer.DelayCalculator()

    print(f"Restarting the server in {ShutdownDelay.totalDelay}")

    try:
        baseMessage = f"Restarting the server for {message}"
    except IndexError:
        baseMessage = f"Restarting the server for a scheduled reboot"

    reboot_intervals = ShutdownDelay.get_all_intervals()
    for x in reboot_intervals:
        if not x == 1:
            fullMessage = " ".join([baseMessage, f"in {x} minutes."])
            send_message(fullMessage)
            time.sleep(300)
        else:
            fullMessage = " ".join([baseMessage, "in 1 minute."])
            send_message(fullMessage)
            time.sleep(30)

    lgsm.save_server()
    
    time.sleep(30)

    services.MainServices("stop")

    if backup:
        tools_backup.main()

    services.MainServices("start")

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])