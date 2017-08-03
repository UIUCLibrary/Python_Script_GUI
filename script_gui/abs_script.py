import abc
import logging
import warnings
import threading
import typing

from script_gui.script_args import ArgumentBuilder
from script_gui.script_runners import abs_script_runner
from . import script_args
from PyQt5.QtCore import pyqtSignal, QObject
from .script_signals import SignalTypes


class AbsScript2(metaclass=abc.ABCMeta):
    title = "Python Script"

    def __init__(self):
        self.args = {
            "required": self._build_args(self.required_arguments),
            "optional": self._build_args(self.optional_arguments)
        }
        self.logger = logging.getLogger(self.__class__.__module__)
        self.logger.setLevel(logging.INFO)
        self._abort_flag = threading.Event()
        self._signal_caller = abs_script_runner.NoSignals()
        self.setup()

    def setup(self):
        pass

    @property
    def required_arguments(self) -> typing.List[dict]:
        return []

    @property
    def optional_arguments(self) -> typing.List[dict]:
        return []

    @staticmethod
    def _build_args(arg_list):
        builder = ArgumentBuilder()
        for arg in arg_list:
            builder.add_argument(**arg)
        return builder.build()

    @abc.abstractmethod
    def run(self):
        pass

    def valid(self):
        return True

    def set_logger(self, logger):
        self.logger = logger
        pass

    def set_abort_flag(self, value):
        self._abort_flag = value

    def set_signal_caller(self, value):
        self._signal_caller = value

    def announce(self, signal: SignalTypes, message=None):
        self._signal_caller.CHANGE.emit(signal, message)



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
        warnings.warn("Use AbsScript2 instead", DeprecationWarning)
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
