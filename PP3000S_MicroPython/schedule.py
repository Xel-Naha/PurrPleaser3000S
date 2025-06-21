import time
import json
from config import FEED_TIMES, FEED_AMOUNTS, TREAT_AMOUNT


DEFAULT_AMOUNTS = list(FEED_AMOUNTS) if len(FEED_AMOUNTS) == len(FEED_TIMES) else [TREAT_AMOUNT for _ in FEED_TIMES]
SCHEDULE_FILE = "schedule.json"

class Schedule:
    """Manage feeding schedule and persistence."""

    def __init__(self):
        self.feed_times = list(FEED_TIMES)
        self.amounts = list(DEFAULT_AMOUNTS)
        self.last_feed = None
        self.load()

    def load(self):
        try:
            with open(SCHEDULE_FILE, "r") as f:
                data = json.load(f)
                self.feed_times = data.get("times", self.feed_times)
                self.amounts = data.get("amounts", self.amounts)
        except OSError:
            # File not present; will use defaults
            pass

    def save(self):
        data = {"times": self.feed_times, "amounts": self.amounts}
        with open(SCHEDULE_FILE, "w") as f:
            json.dump(data, f)

    def next_event(self):
        tm = time.localtime()
        now_minutes = tm[3] * 60 + tm[4]
        for idx, (h, m) in enumerate(self.feed_times):
            if now_minutes <= h * 60 + m:
                return idx, h, m, self.amounts[idx]
        return 0, self.feed_times[0][0], self.feed_times[0][1], self.amounts[0]

    def should_feed(self):
        tm = time.localtime()
        for idx, (h, m) in enumerate(self.feed_times):
            if tm[3] == h and tm[4] == m:
                key = (idx, tm[2])
                if self.last_feed != key:
                    self.last_feed = key
                    return True, self.amounts[idx]
        return False, 0

    def set_amount(self, idx, grams):
        if 0 <= idx < len(self.amounts):
            self.amounts[idx] = grams
            self.save()

    def set_time(self, idx, hour, minute):
        if 0 <= idx < len(self.feed_times):
            self.feed_times[idx] = [hour, minute]
            self.save()
