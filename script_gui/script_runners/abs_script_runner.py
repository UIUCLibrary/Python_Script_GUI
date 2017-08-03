import abc
import logging

import sys
from PyQt5.QtCore import pyqtSignal, QObject
from script_gui.script_signals import SignalTypes
# from script_gui.abs_script import AbsScript2
import threading


class NoOpSignal:
    def connect(self):
        pass

    def emit(self, *args, **kwargs):
        pass


class NoSignals:
    HALT = NoOpSignal()
    CHANGE = NoOpSignal()


class ScriptRunner(metaclass=abc.ABCMeta):
    signals = NoSignals()

    def __init__(self, script: "AbsScript2"):
        self.logger = self.configure_logger()
        self._thread_runner = threading.Thread()
        self._abort_flag = threading.Event()
        self.script = script
        self.script.set_abort_flag(self._abort_flag)

    @property
    def title(self) -> str:
        return self.script.title

    def exec_script(self):
        return self.script

    def start(self, daemon=False):
        self.logger.debug("Starting script")
        if daemon:
            self._thread_runner = threading.Thread(target=self.script.run)
            self._thread_runner.daemon = True
            self._thread_runner.start()
        else:
            self.script.run()

    def is_running(self) -> bool:
        return self._thread_runner.is_alive()

    def abort(self, reason=None):
        # TODO set up abort reason
        self._abort_flag.set()

    def reset(self):
        self._abort_flag.clear()

    @abc.abstractmethod
    def configure_logger(self,level=logging.INFO):
        pass
