class Timeline:
    def __init__(self):
        self._time = 0.0
        self._events = []
        self._is_running = True

    def start(self):
        self._is_running = True

    def stop(self):
        self._is_running = False

    def update(self, dt):
        if not self._is_running:
            return

        self._time += dt

        for i, (t, callback) in enumerate(self._events):
            if t <= self._time:
                callback()
                del self._events[i]

    def add(self, time, callback):
        self._events.append((time, callback))


class TimelineLoop:
    def __init__(self, max_time: float):
        self._time = 0.0
        self._max_time = max_time
        self._events = []
        self._removed = []

    def update(self, dt):
        self._time += dt

        if self._time >= self._max_time:
            self._time = 0
            self._events.extend(self._removed)
            self._removed.clear()

        for i, (t, callback) in enumerate(self._events):
            if t <= self._time:
                callback()
                self._removed.append(self._events[i])
                del self._events[i]

    def add(self, time, callback):
        self._events.append((time, callback))
