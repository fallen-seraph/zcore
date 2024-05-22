from math import ceil
from time import time

class apa_timers:
    def __init__(self, minutesUntilRestart=15):
        self._interval = ceil(minutesUntilRestart/3)
        self._targetTime = ceil(time()+minutesUntilRestart*60)


#keeping for reference
#======================================================================================================================
# async def execute_pzrestart(message, timeTill, bot):
#     print(f"Restarting the server in {timeTill} with message: \"{message}\"")

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
