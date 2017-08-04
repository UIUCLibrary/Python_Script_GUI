from PyQt5.QtCore import QObject, pyqtSignal

from script_gui.script_runners import abs_script_runner
# from script_gui import abs_script
import logging
import PyQt5

from script_gui.script_signals import SignalTypes


class QTSignals(QObject):
    HALT = pyqtSignal()
    CHANGE = pyqtSignal(SignalTypes, str)


class QtScriptRunner(abs_script_runner.absScriptRunner):
    signals = QTSignals()

    def __init__(self, script: "AbsScript2"):
        super().__init__(script)
        self.script.set_signal_caller(self.signals)

    def configure_logger(self,level=logging.INFO):
        logger = logging.getLogger(__name__)
        logger.setLevel(level)

        return logger