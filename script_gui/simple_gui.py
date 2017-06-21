import abc
import sys
import functools
import logging
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot
import script_gui
from . import abs_script
from . import gui
from . import gui_logger
from . import states



class SimpleGui(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    abort_signal = pyqtSignal()

    def __init__(self, script: abs_script.AbsScript):
        self.app = QtWidgets.QApplication(sys.argv)
        super().__init__()
        self.statusBar = QtWidgets.QStatusBar()
        self.script = script
        self.abort_signal.connect(self.script.abort)
        self.script.halted_signal.connect(lambda: self.current_state.confirm_finished())
        self.setupUi(self)
        self.startButton.clicked.connect(self.process)
        self.stopButton.clicked.connect(self.abort)
        self.setWindowTitle(self.script.title)
        self.gui_logger = logging.getLogger(__name__)
        self.gui_logger.setLevel(logging.INFO)
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("{} started".format(self.script.title))
        self.all_states = {
            "idle": states.IdleState(self),
            "working": states.WorkingState(self),
            "halting": states.HaltingState(self),
        }

        self.current_state = self.all_states["idle"]
        self.current_state.enter()

    def load_logger(self, debug=False):
        qt_logger = gui_logger.QtLogger(self.textBrowser)
        self.script.logger.addHandler(qt_logger)

        self.gui_logger.addHandler(qt_logger)
        if debug:
            self.gui_logger.setLevel(logging.DEBUG)

    def display(self):
        self.gui_logger.debug("Displaying GUI")
        self.show()
        self.app.exec_()

    def process(self):
        self.gui_logger.debug("Script processing requested by user")
        self.current_state.process()

    def abort(self):
        self.gui_logger.debug("Abort processing requested by user")
        self.current_state.abort()

    def _execute(self):
        self.script.start()
