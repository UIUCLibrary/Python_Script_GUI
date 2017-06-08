import random
import threading
from time import sleep

import logging
from PyQt5 import QtWidgets

import gui
import simple_gui
import abs_script
import gui_logger


class MyScript(abs_script.AbsScript):
    def _script(self):
        while True:
            # while not stopper.is_set():
            text_block = "ASDFasdfasdfacviewnqwerf"
            a = random.randrange(1, len(text_block))
            print("asdasd")
            b = "".join(random.sample(text_block, len(text_block)))
            self.logger.info("Sample message: Random text \"{}\"".format(b[0:a]))
            sleep(.1)

    def run(self):
        self._script()

    def start(self):
        print("Starting")
        self.t = threading.Thread(target=self._script, daemon=True)
        self.t.start()


    @property
    def title(self) -> str:
        return "Garbage Maker"


class MyScriptGUI(simple_gui.SimpleGui):
    def process(self):
        self.script.start()
        pass


def main():
    print("Hello ", __file__)
    script = MyScript()
    # script.run()
    logger = logging.getLogger(__name__)

    app = MyScriptGUI(script)
    app.load_logger(logger)
    # print(script.title)
    app.display()


if __name__ == '__main__':
    main()
