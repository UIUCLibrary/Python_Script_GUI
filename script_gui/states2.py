import abc
from script_gui import simple_gui
from PyQt5.QtWidgets import QMessageBox
from .script_signals import SignalTypes

class AbsState(metaclass=abc.ABCMeta):
    def __init__(self, context: "simple_gui.SimpleGui2"):
        self._gui = context

    @abc.abstractmethod
    def enter(self):
        self._gui.statusBar.showMessage("Status: {}".format(self._gui.current_state.name.title()))
        pass

    @abc.abstractmethod
    def process(self):
        pass

    @abc.abstractmethod
    def abort(self):
        pass

    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    def status_update(self, status, message):
        if isinstance(message, str) and message.strip() == "":
            details = None
        else:
            details = message
        self.confirm_finished()
        if status == SignalTypes.SUCCESS:
            self._gui.announce_success(details)
        elif status == SignalTypes.FAILED:
            self._gui.announce_failure(details)

    def confirm_finished(self):
        pass


class IdleState(AbsState):
    def enter(self):
        super().enter()
        self._gui.startButton.setEnabled(True)
        self._gui.stopButton.setEnabled(False)
        for _, arg_input in self._gui.arg_input.items():
            arg_input.setEnabled(True)

    def process(self):
        if self._gui.script_runner.script.valid:
            self._gui.current_state = self._gui.all_states['working']
            self._gui.current_state.enter()
        else:
            error = QMessageBox(self._gui)
            error.setModal(True)
            error.setWindowTitle("Unable to Start")
            error.setText("Not all required arguments are correctly set.")
            error.setIcon(QMessageBox.Warning)
            error.setDetailedText("Invalid or missing input for {}.".format(", ".join(self._gui.script.args.missing)))
            error.exec()
            pass

    @property
    def name(self) -> str:
        return "idle"

    def abort(self):
        self._gui.gui_logger.error("No process running")


class WorkingState(AbsState):

    def enter(self):
        super().enter()
        self._gui.gui_logger.info("Starting process")
        self._gui.startButton.setEnabled(False)
        self._gui.stopButton.setEnabled(True)
        for _, arg_input in self._gui.arg_input.items():
            arg_input.setEnabled(False)
        self._gui._execute()

    def process(self):
        self._gui.gui_logger.error("Unable to start a new process while running")

    @property
    def name(self) -> str:
        return "working"

    def abort(self):
        self._gui.gui_logger.info("Attempting to stop process")
        self._gui.current_state = self._gui.all_states['halting']
        self._gui.current_state.enter()

    def confirm_finished(self):

        self._gui.gui_logger.info("Job finished")
        self._gui.current_state = self._gui.all_states['idle']
        self._gui.script_runner.reset()
        self._gui.current_state.enter()


class HaltingState(AbsState):

    def enter(self):
        super().enter()
        self._gui.stopButton.setEnabled(False)
        self._gui.abort_signal.emit()

    def process(self):
        self._gui.gui_logger.error("Unable to start a new process until current one has stopped")

    @property
    def name(self) -> str:
        return "halting"

    def abort(self):
        self._gui.gui_logger.error("Already currently trying stop.")

    def confirm_finished(self):
        self._gui.gui_logger.info("process has stopped")
        self._gui.current_state = self._gui.all_states['idle']
        self._gui.script_runner.reset()
        self._gui.current_state.enter()
