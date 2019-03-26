#######################################################################################################################
# timer.py
#
# Simple timer class that is currently not being used. Meant to stop people from accidentally taking multiple pictures
#
# Created by James Brock for Scott Hawley's Physics for AET class
#######################################################################################################################

import time


class Timer:

    def __init__(self):
        self.lastTime = time.time()

    # Returns True if more than a second has passed since the initialization or the last True return of the method
    def hasItBeenASecond(self):
        if (time.time() - self.lastTime) < 1:
            return False
        self.lastTime = time.time()
        return True
