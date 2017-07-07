import abc
import logging
import threading
from  . import args
from PyQt5.QtCore import pyqtSignal, QObject


class AbsScript(QObject):
    halted_signal = pyqtSignal()


    @property
    @abc.abstractmethod
    def title(self) -> str:
        pass

    @abc.abstractmethod
    def run(self):
        pass

    def __init__(self):
        super().__init__()
        self.args = args.Arguments()
        self.t = threading.Thread()
        self._abort_flag = threading.Event()
        self.logger = logging.getLogger(self.__module__)


    @abc.abstractmethod
    def start(self):
        pass

    def abort(self):
        self.logger.debug("Setting abort flag")
        self._abort_flag.set()
        self.logger.debug("Abort flag has been set")

    def is_running(self) -> bool:
        return self.t.is_alive()

    def announce_ended(self):
        self.halted_signal.emit()

    def reset(self):
        self._abort_flag.clear()

