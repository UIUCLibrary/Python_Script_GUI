from time import sleep

import pytest

from script_gui import abs_script
from script_gui.script_runners import abs_script_runner, cli_runner, gui_runner

from PyQt5.QtCore import pyqtSignal, QObject

from script_gui.abs_script import AbsScript2


class NoScript(AbsScript2):
    title = "No script"

    def run(self):
        # todo:  change to run until break
        sleep(1)


def test_is_abstract():
    class DummyAbsScript(abs_script_runner.absScriptRunner):
        pass

    with pytest.raises(TypeError):
        DummyAbsScript(NoScript())


class TestQtScript:
    @pytest.fixture()
    def script_fixture(self):
        return gui_runner.QtScriptRunner(NoScript())

    def test_built(self, script_fixture: gui_runner.QtScriptRunner):
        assert isinstance(script_fixture, gui_runner.QtScriptRunner)

    def test_signals(self, script_fixture: gui_runner.QtScriptRunner):
        assert isinstance(script_fixture.signals, gui_runner.QTSignals)

    def test_title(self, script_fixture: gui_runner.QtScriptRunner):
        assert script_fixture.title == "No script"

    def test_start_daemon(self, script_fixture: gui_runner.QtScriptRunner):
        # FIXME: Very flakey test because it's currently running a thread on a timer.
        script_fixture.start(daemon=True)
        was_running = False
        while script_fixture.is_running():
            was_running = True
            sleep(.1)
        assert script_fixture.is_running() is False
        assert was_running is True


class TestCLIScript:
    @pytest.fixture()
    def script_fixture(self):
        return cli_runner.CLIScriptRunner(NoScript())

    def test_signals(self, script_fixture: cli_runner.CLIScriptRunner):
        assert isinstance(script_fixture.signals,  abs_script_runner.NoSignals)
        assert isinstance(script_fixture.signals.HALT,  abs_script_runner.NoOpSignal)
        assert isinstance(script_fixture.signals.CHANGE, abs_script_runner.NoOpSignal)

    def test_built(self, script_fixture: cli_runner.CLIScriptRunner):
        assert isinstance(script_fixture, cli_runner.CLIScriptRunner)

    def test_title(self, script_fixture: cli_runner.CLIScriptRunner):
        assert script_fixture.title == "No script"

    def test_start_no_daemon(self, script_fixture: cli_runner.CLIScriptRunner):
        script_fixture.start()
        assert script_fixture.is_running() is False
