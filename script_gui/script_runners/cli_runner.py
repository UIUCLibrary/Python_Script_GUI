from script_gui.script_runners import abs_script_runner
import logging


class CLIScriptRunner(abs_script_runner.absScriptRunner):
    def configure_logger(self, level=logging.INFO):
        return logging.getLogger(__name__)
