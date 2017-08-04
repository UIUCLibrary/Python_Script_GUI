import abc
import sys
import functools
import warnings
import logging
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot
import script_gui
from . import abs_script
from . import gui
from . import gui_logger
from . import states
from . import states2
from script_gui.script_runners import abs_script_runner, gui_runner


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


#
# class SimpleGui(QtWidgets.QMainWindow, gui.Ui_MainWindow):
#     abort_signal = pyqtSignal()
#
#     def __init__(self, script: abs_script.AbsScript):
#         warnings.warn("Use SimpleGui2", DeprecationWarning)
#         self.app = QtWidgets.QApplication(sys.argv)
#         super().__init__()
#
#         self.statusBar = QtWidgets.QStatusBar()
#         self.script = script
#         self.abort_signal.connect(self.script.abort)
#
#         self.script.change_signal.connect(lambda status, message: self.current_state.status_update(status, message))
#         self.setupUi(self)
#         self.actionSave_Console_Log.triggered.connect(self.save_console_to_file)
#         self.arg_input = dict()
#
#         if len(self.script.args._required) > 0:
#
#             self.gridLayout.addWidget(QtWidgets.QLabel("Required Arguments:"), 0, 0, 1, 2)
#             # self.formLayout.addRow((QtWidgets.QLabel("Required Arguments:")))
#             start = 1
#             for row, (arg_name, arg_value) in enumerate(self.script.args._required.items()):
#                 new_line_edit = QtWidgets.QLineEdit(self)
#                 new_label = QtWidgets.QLabel(arg_name)
#
#                 new_line_edit.setText(arg_value.value)
#                 new_line_edit.textChanged.connect(
#                     lambda d, arg=arg_name, sender=new_line_edit: self._set_arg(arg, d, sender))
#
#                 if arg_value.help:
#                     new_label.setToolTip(arg_value.help)
#                     new_line_edit.setToolTip(arg_value.help)
#
#                 self.arg_input[arg_name] = new_line_edit
#                 self.gridLayout.addWidget(new_label, row + start, 0)
#                 self.gridLayout.addWidget(new_line_edit, row + start, 1)
#                 # self.formLayout.addRow((new_label), new_line_edit)
#
#         if len(self.script.args._optional) > 0:
#             start = len(self.script.args._required) + 2
#             self.gridLayout.addWidget(QtWidgets.QLabel("Optional Arguments:"), len(self.script.args._required) + 1, 0, 1, 2)
#             for row, (arg_name, arg_value) in enumerate(self.script.args._optional.items()):
#                 new_line_edit = QtWidgets.QLineEdit(self)
#                 new_line_edit.setText(arg_value.value)
#                 new_line_edit.textEdited.connect(
#                     lambda d, arg=arg_name, sender=new_line_edit: self._set_arg(arg, d, sender))
#                 self.arg_input[arg_name] = new_line_edit
#                 self.gridLayout.addWidget(QtWidgets.QLabel(arg_name), row + start, 0)
#                 self.gridLayout.addWidget(new_line_edit, row + start, 1)
#                 # self.formLayout.addRow((QtWidgets.QLabel(arg_name)), new_line_edit)
#
#         self.startButton.clicked.connect(self.process)
#         self.stopButton.clicked.connect(self.abort)
#         self.setWindowTitle(self.script.title)
#         self.gui_logger = logging.getLogger(__name__)
#         self.gui_logger.setLevel(logging.INFO)
#         self.setStatusBar(self.statusBar)
#         self.textBrowser.setFont(QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont))
#         self.statusBar.showMessage("{} started".format(self.script.title))
#         self.all_states = {
#             "idle": states.IdleState(self),
#             "working": states.WorkingState(self),
#             "halting": states.HaltingState(self),
#         }
#
#         self.current_state = self.all_states["idle"]
#         self.current_state.enter()
#
#     def announce_success(self, details=None):
#         message = QtWidgets.QMessageBox(self)
#         message.setModal(True)
#         message.setWindowTitle("Process finished")
#         message.setIcon(QtWidgets.QMessageBox.Information)
#
#         if details is not None:
#             details_width = get_max_line_width(details)
#             margin = 40
#             message.setText(
#                 "Job finished successfully.\nFor more information click the details button below.\n{}".format(
#                     " " * (details_width + margin)))
#             message.setDetailedText(details)
#         else:
#             message.setText("Job finished successfully.")
#         message.exec()
#
#     def announce_failure(self, details=None):
#         error = QtWidgets.QMessageBox(self)
#         error.setModal(True)
#         error.setWindowTitle("Process stopped")
#         error.setText("Script stopped prematurely")
#         error.setIcon(QtWidgets.QMessageBox.Warning)
#         if details is not None:
#             error.setDetailedText(details)
#         error.exec()
#
#     def set_debug(self, set_debug=False):
#         qt_logger = gui_logger.QtLogger(self.textBrowser)
#         self.script.logger.addHandler(qt_logger)
#
#         self.gui_logger.addHandler(qt_logger)
#         if set_debug:
#             self.gui_logger.setLevel(logging.DEBUG)
#
#     def display(self):
#         self.gui_logger.set_debug("Displaying GUI")
#         self.show()
#         self.app.exec_()
#
#     def process(self):
#         self.gui_logger.set_debug("Script processing requested by user")
#         self.current_state.process()
#
#     def abort(self):
#         self.gui_logger.set_debug("Abort processing requested by user")
#         self.current_state.abort()
#
#     def save_console_to_file(self):
#         self.gui_logger.set_debug("Opening Save file dialog box")
#         save_dialog_box = QtWidgets.QFileDialog()
#         filename, _ = save_dialog_box.getSaveFileName(self, filter="Text Files (*.txt);;All Files (*)")
#         if filename:
#             try:
#                 self.gui_logger.set_debug("Save Console output as {}".format(filename))
#                 with open(filename, "w", encoding="utf8") as writer:
#                     writer.write(self.textBrowser.toPlainText())
#                 self.gui_logger.info("Console output saved to {}".format(filename))
#             except IOError as e:
#                 self.gui_logger.error(e)
#
#     def _execute(self):
#         self.script.start()
#
#     def _set_arg(self, name, value, sender):
#         arg = self.script.args[name]
#         arg.value = value
#         if arg.valid:
#             color = "#c4df9b"  # Green
#         else:
#             color = "#f6989d"  # Red
#         sender.setStyleSheet("QLineEdit {{ background-color: {} }}".format(color))




class SimpleGui2(QtWidgets.QMainWindow, gui.Ui_MainWindow):

    def __init__(self, script):
        self.app = QtWidgets.QApplication(sys.argv)
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(script.title)

        self.arg_input = dict()
        self.script_runner = gui_runner.QtScriptRunner(script)

        # Add Additional static Gui Widgets
        self.statusBar = QtWidgets.QStatusBar()

        # Load script arguments
        self.load_arguments(self.script_runner.script.args)

        # Wire up the signals
        self.actionSave_Console_Log.triggered.connect(self.save_console_to_file)
        self.script_runner.signals.CHANGE.connect(
            lambda status, message: self.current_state.status_update(status, message))
        self.startButton.clicked.connect(self.process)
        self.stopButton.clicked.connect(self.abort)

        # Set up Logger
        self.gui_logger = self._create_logger()
        logger_handler = gui_logger.QtLogger(self.textBrowser)
        self._set_log_handlers(self.gui_logger, logger_handler)
        self._set_log_handlers(self.script_runner.logger, logger_handler)
        self._set_log_handlers(self.script_runner.script.logger, logger_handler)
        self.set_debug(False)
        self.setStatusBar(self.statusBar)
        self.textBrowser.setFont(QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont))


        # Set States
        # TODO: refactor state into runner instead of the app
        self.all_states = {
            "idle": states2.IdleState(self),
            "working": states2.WorkingState(self),
            "halting": states2.HaltingState(self),
        }

        self.current_state = self.all_states["idle"]
        self.current_state.enter()


        self.statusBar.showMessage("{} started".format(self.script_runner.title))

    def load_arguments(self, args):
        if len(args["required"]) > 0:

            self.gridLayout.addWidget(QtWidgets.QLabel("Required Arguments:"), 0, 0, 1, 2)
            # self.formLayout.addRow((QtWidgets.QLabel("Required Arguments:")))
            start = 1
            for row, (arg_name, arg_value) in enumerate(args["required"].items()):
                new_line_edit = QtWidgets.QLineEdit(self)
                new_label = QtWidgets.QLabel(arg_name)

                new_line_edit.setText(arg_value.value)
                new_line_edit.textChanged.connect(
                    lambda d, arg=arg_name, sender=new_line_edit: self._set_arg(arg, d, sender))

                if arg_value.help:
                    new_label.setToolTip(arg_value.help)
                    new_line_edit.setToolTip(arg_value.help)

                self.arg_input[arg_name] = new_line_edit
                self.gridLayout.addWidget(new_label, row + start, 0)
                self.gridLayout.addWidget(new_line_edit, row + start, 1)
                # self.formLayout.addRow((new_label), new_line_edit)
        if len(args["optional"]) > 0:
            start = len(args["required"]) + 2
            self.gridLayout.addWidget(QtWidgets.QLabel("Optional Arguments:"),
                                      len(args["required"]) + 1, 0, 1, 2)
            for row, (arg_name, arg_value) in enumerate(args["optional"].items()):
                new_line_edit = QtWidgets.QLineEdit(self)
                new_line_edit.setText(arg_value.value)
                new_line_edit.textEdited.connect(
                    lambda d, arg=arg_name, sender=new_line_edit: self._set_arg(arg, d, sender))
                self.arg_input[arg_name] = new_line_edit
                self.gridLayout.addWidget(QtWidgets.QLabel(arg_name), row + start, 0)
                self.gridLayout.addWidget(new_line_edit, row + start, 1)
                # self.formLayout.addRow((QtWidgets.QLabel(arg_name)), new_line_edit)

    def _create_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        return logger

    def _set_log_handlers(self, logger, logger_handler):
        logger.addHandler(logger_handler)

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

    def set_debug(self, debug=False):

        if debug:
            self.gui_logger.setLevel(logging.DEBUG)
            debug_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            for x in self.gui_logger.handlers:
                x.setFormatter(debug_format)
                # std_logger.setFormatter(debug_format)
        else:
            self.gui_logger.setLevel(logging.INFO)

    def display(self):
        self.gui_logger.debug("Displaying GUI")
        self.show()
        self.app.exec_()

    def process(self):
        self.gui_logger.debug("Script processing requested by user")
        self.current_state.process()

    def abort(self):
        self.gui_logger.debug("Abort processing requested by user")
        try:
            self.current_state.abort()
        except Exception as e:
            print(e)
            raise

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
        self.script_runner.start(daemon=True)

    def _set_arg(self, name, value, sender):
        def get_arg():
            # TODO: Ugly Code! Refactor when given a chance
            if name in self.script_runner.script.args["required"]:
                return self.script_runner.script.args["required"][name]
            if name in self.script_runner.script.args["optional"]:
                return self.script_runner.script.args["optional"][name]

        arg = get_arg()
        # arg =
        arg.value = value
        if arg.valid:
            color = "#c4df9b"  # Green
        else:
            color = "#f6989d"  # Red
        sender.setStyleSheet("QLineEdit {{ background-color: {} }}".format(color))
