import abc
import sys

import logging
from PyQt5 import QtWidgets
import gui
import gui_logger
import abs_script


# class AbsSimpleGui(metaclass=abc.ABCMeta):
#     @abc.abstractmethod
#     def process(self):
#         pass
#
#     @abc.abstractmethod
#     def run(self):
#         pass


class SimpleGui(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self, script):
        self.app = QtWidgets.QApplication(sys.argv)
        super().__init__()
        self.script = script
        self.setupUi(self)
        self.pushButton.clicked.connect(self.process)
        self.setWindowTitle(self.script.title)

    def load_logger(self, logger):
        print("starting gui logger")
        # logger = logging.getLogger(__name__)
        qt_logger = gui_logger.QtLogger(self.textBrowser)
        logger.addHandler(qt_logger)

    def display(self):

        self.show()
        self.app.exec_()
