import abc
from . import abs_script_runner


class AbsRunnerState(metaclass=abc.ABCMeta):
    name = "AbsRunnerState"

    def __init__(self, context: "abs_script_runner.absScriptRunner"):
        self._context = context

    def setup(self):
        self._context.logger.debug("setting up {}".format(self.__class__))
        pass

    @abc.abstractmethod
    def abort(self, reason=None):
        pass

    @abc.abstractmethod
    def reset(self):
        pass

    @abc.abstractmethod
    def start(self, daemon=False):
        pass

    def teardown(self):
        pass


class IdleState(AbsRunnerState):
    name = "idle"

    def start(self, daemon=False):
        self._context.exec(daemon)
        self._context.change_state("running")

    def reset(self):
        raise RuntimeError("Already Idle")

    def abort(self, reason=None):
        raise RuntimeError("Already Idle")


class RunningState(AbsRunnerState):
    name = "running"

    def start(self, daemon=False):
        raise RuntimeError("Already running")

    def abort(self, reason=None):
        self._context.change_state("halting")

    def reset(self):
        raise RuntimeError("Unable to reset when running")


class HaltingState(AbsRunnerState):
    name = "halting"

    def setup(self):
        self._context.signals.HALT.emit()
        self._context._abort_flag.set()

    def reset(self):
        # self._context._abort_flag.clear()
        self._context.change_state("failed")

    def start(self, daemon=False):
        raise RuntimeError("Unable to start until is idle")

    def abort(self, reason=None):
        raise RuntimeError("Already halting")


class CompletedState(AbsRunnerState):
    name = "completed"

    def setup(self):
        self._context._abort_flag.clear()

    def start(self, daemon=False):
        raise RuntimeError("Unable to start after finishing")

    def reset(self):
        self._context.change_state("idle")

    def abort(self, reason=None):
        raise RuntimeError("Unable to abort after finishing")


class FailedState(AbsRunnerState):
    name = "failed"

    def setup(self):
        self._context._abort_flag.clear()

    def start(self, daemon=False):
        raise RuntimeError("Unable to start after finishing")

    def reset(self):
        self._context.change_state("idle")

    def abort(self, reason=None):
        raise RuntimeError("Unable to abort after finishing")
