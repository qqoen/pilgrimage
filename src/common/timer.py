class Timer:
    def __init__(self, duration, autostart=False):
        self._duration = duration
        self._time_left = 0.0

        if autostart:
            self.start()

    @property
    def finished(self):
        return self._time_left == 0

    @property
    def duration(self):
        return self._duration

    @property
    def time_left(self):
        return self._time_left

    def start(self):
        self._time_left = self._duration

    def finish(self):
        self._time_left = 0

    def update(self, dt: float):
        self._time_left = max(0, self._time_left - dt)
