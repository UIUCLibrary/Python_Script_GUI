import abc
import logging
import threading


class AbsScript(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def title(self) -> str:
        pass

    @abc.abstractmethod
    def run(self):
        pass

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.t = threading.Thread()
