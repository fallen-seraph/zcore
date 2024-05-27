import math
import time

class DelayCalculator:
    def __init__(self, minutesUntilRestart=15):
        self.minutesUntilRestart = minutesUntilRestart
        self._intervalCount = math.ceil(self.minutesUntilRestart/5)
        self._totalDelay = self._intervalCount*5

    @property
    def intervalCount(self):
        return self.minutesUntilRestart
    
    @property
    def totalDelay(self):
        return self._totalDelay

    def get_interval_time(self):
        return (self._intervalCount*5)/5
    
    def getTargetTime(self):
        return math.ceil(time.time()+self.minutesUntilRestart*60)
    
    def get_all_intervals(self):
        intervals = []
        for x in range(self._intervalCount):
            y = self._totalDelay-(x*5)
            if not y == 0: 
                intervals.append(y)
        intervals.append(1)
        return intervals