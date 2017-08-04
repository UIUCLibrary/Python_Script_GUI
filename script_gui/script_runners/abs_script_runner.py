import abc
import logging

import sys
from PyQt5.QtCore import pyqtSignal, QObject
from script_gui.script_signals import SignalTypes
# from script_gui.abs_script import AbsScript2
from script_gui import abs_script
from . import states
import threading


class NoOpSignal:
    def connect(self):
        pass

    def emit(self, *args, **kwargs):
        pass


class NoSignals:
    HALT = NoOpSignal()
    CHANGE = NoOpSignal()


class JobThread(threading.Thread):
    def __init__(self, runner=None, callback=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.runner = runner
        self.callback = callback

    def run(self):
        self.runner.script.run()
        if self.callback:
            self.callback()


class absScriptRunner(metaclass=abc.ABCMeta):
    signals = NoSignals()

    def __init__(self, script: "abs_script.AbsScript2"):
        self.logger = self.configure_logger()
        self._thread_runner = JobThread()
        self._abort_flag = threading.Event()
        self.script = script
        self.script.set_abort_flag(self._abort_flag)
        self.all_states = {
            "idle": states.IdleState(self),
            "running": states.RunningState(self),
            "halting": states.HaltingState(self),
            "completed": states.CompletedState(self),
            "failed": states.FailedState(self),
        }
        self.current_state = self.all_states["idle"]

    def change_state(self, state_name: str):
        self.current_state.teardown()
        try:
            self.current_state = self.all_states[state_name]
        except KeyError:
            print("Invalid state {}".format(state_name))
            raise KeyError("Invalid state {}".format(state_name))
        self.current_state.setup()

    @property
    def title(self) -> str:
        return self.script.title

    def exec_script(self):
        return self.script

    def start(self, daemon=False):
        self.current_state.start(daemon)

    def exec(self, daemon: bool):
        """Execute the script, either threaded or not threaded.

        Notes:
            This should not be used directly to execute the script. To make sure that states are followed,
            use the start method instead.

        Args:
            daemon: Run script blocked or on a separate thread.


        """
        self.logger.debug("Starting script")
        if daemon:
            self._thread_runner = JobThread(self)
            # self._thread_runner.runner = self
            self._thread_runner.daemon = True
            self._thread_runner.start()
        else:
            self.script.run()

    def is_running(self) -> bool:
        return self._thread_runner.is_alive()

    def abort(self, reason=None):
        self.current_state.abort(reason)
        # TODO set up abort reason

    def reset(self):
        self.current_state.reset()

    @abc.abstractmethod
    def configure_logger(self, level=logging.INFO):
        pass
