import time
from config import FEED_TIMES

class Schedule:
    def __init__(self):
        self.feed_times = FEED_TIMES
        self.last_feed = None

    def should_feed(self):
        tm = time.localtime()
        for h, m in self.feed_times:
            if tm[3] == h and tm[4] == m:
                if self.last_feed != (h, m, tm[2]):
                    self.last_feed = (h, m, tm[2])
                    return True
        return False
