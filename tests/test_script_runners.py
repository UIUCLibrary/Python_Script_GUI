# TODO create test for test runner states
from script_gui import script_runners
from script_gui.script_runners import gui_runner
from script_gui import abs_script
import pytest


class MockScript(abs_script.AbsScript2):
    def run(self):
        pass


class MockScriptRunner(gui_runner.QtScriptRunner):
    def force_success(self):
        if not self.current_state.name == "running":
            raise Exception
        self.change_state("completed")

    def force_shutdown_on_failure(self):
        if not self.current_state.name == "halting":
            raise Exception()
        self.change_state("failed")


class TestQtRunner:
    @pytest.fixture()
    def qt_fixture(self):
        mock_script = MockScript()
        return MockScriptRunner(mock_script)

    def test_qt(self, qt_fixture):
        assert isinstance(qt_fixture, gui_runner.QtScriptRunner)


class TestScriptRunnerState:
    @pytest.fixture()
    def fixture(self):
        mock_script = MockScript()
        return MockScriptRunner(mock_script)

    def test_idle_state(self, fixture: MockScriptRunner):
        assert isinstance(fixture.current_state, script_runners.IdleState)

    def test_running_state(self, fixture: MockScriptRunner):
        fixture.start()
        assert isinstance(fixture.current_state, script_runners.RunningState)

    def test_running_state_reset(self, fixture: MockScriptRunner):
        # You can't reset if the script running is already running
        fixture.start()
        with pytest.raises(RuntimeError):
            print("Sending an invalid reset request")
            fixture.reset()

    def test_halting_state(self, fixture: MockScriptRunner):
        fixture.start()
        fixture.abort()
        assert isinstance(fixture.current_state, script_runners.HaltingState)

    def test_running_finished(self, fixture: MockScriptRunner):
        fixture.start()
        fixture.force_success()
        assert isinstance(fixture.current_state, script_runners.CompletedState)

    def test_halting_goes_to_failed(self, fixture: MockScriptRunner):
        fixture.start()
        fixture.abort()
        fixture.force_shutdown_on_failure()
        assert isinstance(fixture.current_state, script_runners.FailedState)
