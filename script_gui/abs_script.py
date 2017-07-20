import abc
import logging
import warnings
import threading
from . import script_args
from PyQt5.QtCore import pyqtSignal, QObject
from .script_signals import SignalTypes


class AbsScript(QObject):
    _halted_signal = pyqtSignal()
    change_signal = pyqtSignal(SignalTypes, str)

    @property
    @abc.abstractmethod
    def title(self) -> str:
        pass

    @abc.abstractmethod
    def run(self):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = script_args.Arguments()
        self.t = threading.Thread()
        self._abort_flag = threading.Event()
        if "logger" in kwargs:
            self.logger = logging.getLogger(kwargs["logger"])
        else:
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
        warnings.warn("Use announce instead", DeprecationWarning)
        self.halted_signal.emit()

    def announce(self, signal: SignalTypes, message=None):
        self.change_signal.emit(signal, message)

    def reset(self):
        self._abort_flag.clear()

    @property
    def halted_signal(self):
        warnings.warn("Use change_signal instead", DeprecationWarning)
        return self._halted_signal
