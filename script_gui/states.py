import abc
from script_gui import simple_gui


class AbsState(metaclass=abc.ABCMeta):
    def __init__(self, context: "simple_gui.SimpleGui"):
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

    def confirm_finished(self):
        pass


class IdleState(AbsState):
    def enter(self):
        super().enter()
        self._gui.startButton.setEnabled(True)
        self._gui.stopButton.setEnabled(False)

    def process(self):
        self._gui.current_state = self._gui.all_states['working']
        self._gui.current_state.enter()


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
        pass


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
        self._gui.script.reset()
        self._gui.current_state.enter()
