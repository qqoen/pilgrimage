from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def draw(self):
        pass


class StateMachine:
    def __init__(self):
        self._state_types = {}
        self._state: State | None = None

    def register(self, state_name: str, constructor):
        if state_name in self._state_types:
            raise ValueError(f"State '{state_name}' is already registered.")
        self._state_types[state_name] = constructor

    def switch(self, state_name: str, **payload):
        if state_name not in self._state_types:
            raise ValueError(f"State '{state_name}' is not registered.")
        self._state = self._state_types[state_name](payload)

    def update(self, dt: float):
        if self._state is not None:
            self._state.update(dt)

    def draw(self):
        if self._state is not None:
            self._state.draw()

