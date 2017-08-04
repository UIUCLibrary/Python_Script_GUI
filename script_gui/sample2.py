import logging
import random
import threading
import typing
from time import sleep

import sys

from script_gui.abs_script import AbsScript2
from script_gui.script_runners import cli_runner, gui_runner
from script_gui.script_runners.abs_script_runner import absScriptRunner
from script_gui.simple_gui import SimpleGui2
from script_gui.script_signals import SignalTypes


class MyScript(AbsScript2):
    title = "Garbage"

    def run(self):

        self.logger.info("HERE we go")
        keep_going = True
        while keep_going:
            if self._abort_flag.is_set():
                self.announce(SignalTypes.FAILED)
                break
            # # while not self._abort_flag.is_set():
            text_block = "ASDFasdfasdfacviewnqwerf"
            a = random.randrange(1, len(text_block))
            b = "".join(random.sample(text_block, len(text_block)))
            self.logger.info("Sample message: Random text \"{}\"".format(b[0:a]))
            sleep(.5)
            keep_going = False
        else:
            self.announce(SignalTypes.SUCCESS)

    @property
    def required_arguments(self) -> typing.List[dict]:
        required = [
            {
                "name": "foo",
                "default": "aaaaa",
                "help": "something"
            },
            {
                "name": "Bar",
                "default": "f",
                "validate": lambda user_data: user_data == "f"

            }

        ]
        return required

    @property
    def optional_arguments(self) -> typing.List[dict]:
        return [
            {
                "name": "Baz"
            }
        ]


def main():
    print("Hello ", __file__)
    my_script = MyScript()
    # my_script.logger.addHandler(std_logger)

    app = SimpleGui2(script=my_script)
    # app.gui_logger.addHandler(std_logger)
    app.set_debug(debug=True)
    app.display()


if __name__ == '__main__':
    main()
