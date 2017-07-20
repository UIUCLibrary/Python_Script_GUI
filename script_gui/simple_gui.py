import abc
import sys
import functools
import logging
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot
import script_gui
from . import abs_script
from . import gui
from . import gui_logger
from . import states


#
# def catch_exceptions(t, val, tb):
#     print("EXCEPTION")
#     QtWidgets.QMessageBox.critical(None,
#                                    "An exception was raised",
#                                    "Exception type: {}".format(t))
# old_hook = sys.excepthook
# sys.excepthook = catch_exceptions

def get_max_line_width(text):
    max_len = 0
    for line in text.split("\n"):
        if len(line) > max_len:
            max_len = len(line)

    return max_len


class SimpleGui(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    abort_signal = pyqtSignal()

    def __init__(self, script: abs_script.AbsScript):
        self.app = QtWidgets.QApplication(sys.argv)
        super().__init__()

        self.statusBar = QtWidgets.QStatusBar()
        self.script = script
        self.abort_signal.connect(self.script.abort)

        self.script.change_signal.connect(lambda status, message: self.current_state.status_update(status, message))
        self.setupUi(self)
        self.actionSave_Console_Log.triggered.connect(self.save_console_to_file)
        self.arg_input = dict()

        if len(self.script.args._required) > 0:
            self.formLayout.addRow((QtWidgets.QLabel("Required Arguments:")))
            for arg_name, arg_value in self.script.args._required.items():
                new_line_edit = QtWidgets.QLineEdit(self)
                new_label = QtWidgets.QLabel(arg_name)

                new_line_edit.setText(arg_value.value)
                new_line_edit.textChanged.connect(
                    lambda d, arg=arg_name, sender=new_line_edit: self._set_arg(arg, d, sender))

                if arg_value.help:
                    new_label.setToolTip(arg_value.help)
                    new_line_edit.setToolTip(arg_value.help)

                self.arg_input[arg_name] = new_line_edit

                self.formLayout.addRow((new_label), new_line_edit)

        if len(self.script.args._optional) > 0:
            self.formLayout.addRow((QtWidgets.QLabel("Optional Arguments:")))
            for arg_name, arg_value in self.script.args._optional.items():
                new_line_edit = QtWidgets.QLineEdit(self)
                new_line_edit.setText(arg_value.value)
                new_line_edit.textEdited.connect(
                    lambda d, arg=arg_name, sender=new_line_edit: self._set_arg(arg, d, sender))
                self.arg_input[arg_name] = new_line_edit
                self.formLayout.addRow((QtWidgets.QLabel(arg_name)), new_line_edit)

        self.startButton.clicked.connect(self.process)
        self.stopButton.clicked.connect(self.abort)
        self.setWindowTitle(self.script.title)
        self.gui_logger = logging.getLogger(__name__)
        self.gui_logger.setLevel(logging.INFO)
        self.setStatusBar(self.statusBar)
        self.textBrowser.setFont(QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont))
        self.statusBar.showMessage("{} started".format(self.script.title))
        self.all_states = {
            "idle": states.IdleState(self),
            "working": states.WorkingState(self),
            "halting": states.HaltingState(self),
        }

        self.current_state = self.all_states["idle"]
        self.current_state.enter()

    def announce_success(self, details=None):
        message = QtWidgets.QMessageBox(self)
        message.setModal(True)
        message.setWindowTitle("Process finished")
        message.setIcon(QtWidgets.QMessageBox.Information)

        if details is not None:
            details_width = get_max_line_width(details)
            margin = 40
            message.setText(
                "Job finished successfully.\nFor more information click the details button below.\n{}".format(
                    " " * (details_width + margin)))
            message.setDetailedText(details)
        else:
            message.setText("Job finished successfully.")
        message.exec()

    def announce_failure(self, details=None):
        error = QtWidgets.QMessageBox(self)
        error.setModal(True)
        error.setWindowTitle("Process stopped")
        error.setText("Script stopped prematurely")
        error.setIcon(QtWidgets.QMessageBox.Warning)
        if details is not None:
            error.setDetailedText(details)
        error.exec()

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

    def save_console_to_file(self):
        self.gui_logger.debug("Opening Save file dialog box")
        save_dialog_box = QtWidgets.QFileDialog()
        filename, _ = save_dialog_box.getSaveFileName(self, filter="Text Files (*.txt);;All Files (*)")
        if filename:
            try:
                self.gui_logger.debug("Save Console output as {}".format(filename))
                with open(filename, "w", encoding="utf8") as writer:
                    writer.write(self.textBrowser.toPlainText())
                self.gui_logger.info("Console output saved to {}".format(filename))
            except IOError as e:
                self.gui_logger.error(e)

    def _execute(self):
        self.script.start()

    def _set_arg(self, name, value, sender):
        arg = self.script.args[name]
        arg.value = value
        if arg.valid:
            color = "#c4df9b"  # Green
        else:
            color = "#f6989d"  # Red
        sender.setStyleSheet("QLineEdit {{ background-color: {} }}".format(color))
