from math import ceil
from time import time

class apa_timers:
    def __init__(self, minutesUntilRestart=15):
        self._interval = ceil(minutesUntilRestart/3)
        self._targetTime = ceil(time()+minutesUntilRestart*60)