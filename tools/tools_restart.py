import tools.linux_services as services
import tools.tools_lgsm as lgsm
import tools.tools_timer as tools_timer
import tools.tools_backup as tools_backup
import time
import sys

def send_message(fullMessage):
    lgsm.send_server_message(fullMessage)


def main(message, delay, backup):
    try:
        ShutdownDelay = tools_timer.DelayCalculator(int(delay))
    except ValueError as verr:
            sys.exit(f"{verr}")
    except IndexError:
        ShutdownDelay = tools_timer.DelayCalculator()
    except TypeError:
        ShutdownDelay = tools_timer.DelayCalculator()

    print(f"Restarting the server in {ShutdownDelay.totalDelay}")

    if message:
        baseMessage = f"Restarting the server for {message}"
    else:
        baseMessage = "Restarting the server for a scheduled reboot"

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