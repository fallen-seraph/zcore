import linux_services as services
import tools_lgsm as lgsm
import tools.timer as timer
import tools.tools_backup as tools_backup
import time
import sys

def send_discord_message(message):
     print("sending message")

def main(message, delay, backup):
    try:
        ShutdownDelay = timer.DelayCalculator(int(delay))
    except ValueError as verr:
            sys.exit(f"{verr}")
    except IndexError:
        ShutdownDelay = timer.DelayCalculator()

    print(f"Restarting the server in {ShutdownDelay.totalDelay}")

    try:
        message = f"Restarting the server for {message}"
    except IndexError:
        message = f"Restarting the server for a scheduled reboot"

    reboot_intervals = ShutdownDelay.get_all_intervals()
    for x in reboot_intervals:
        if not x == 1:
            message = " ".join([message, f"in {x} minutes."])
            time.sleep(300)
        else:
            message = " ".join([message, "in 1 minute."])
            time.sleep(30)

    lgsm.save_server()
    
    time.sleep(30)

    services.MainServices("stop")

    if backup:
        tools_backup.main()

    services.MainServices("start")



#keeping for reference
#======================================================================================================================
# async def execute_pzrestart(message, timeTill, bot):

#     timeTill = int(timeTill)

#     if (timeTill != 0):
#         interval = math.ceil(timeTill/3)
#         loopCounter = 0

#         while(loopCounter < 3):
#             await execute_sendMessage(f"Restarting the server for {message} in {timeTill} minute(s).", bot)
#             timeTill = timeTill - interval
#             loopCounter += 1
#             await asyncio.sleep(interval*60)

#         execute_save()

#         await asyncio.sleep(30)

#         execute_restart()
#     else:
#         execute_save()

#         await asyncio.sleep(30)
    
#         execute_restart()


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])