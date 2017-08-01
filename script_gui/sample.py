import logging
import random
import threading
from time import sleep

from script_gui import SimpleGui, AbsScript
from script_gui.script_signals import SignalTypes


class MyScript(AbsScript):
    def _script(self):
        # logger = logging.getLogger(__name__)
        keep_going = True
        while keep_going:
            if self._abort_flag.is_set():
                self.announce(SignalTypes.FAILED)
                break
                # while not self._abort_flag.is_set():
            text_block = "ASDFasdfasdfacviewnqwerf"
            a = random.randrange(1, len(text_block))
            b = "".join(random.sample(text_block, len(text_block)))
            self.logger.info("Sample message: Random text \"{}\"".format(b[0:a]))
            # sleep(.5)
            keep_going = False
        else:
            self.announce(SignalTypes.SUCCESS)

    def run(self):
        self._script()

    def start(self):
        self.t = threading.Thread(target=self._script, daemon=True)
        self.t.start()

    def __init__(self):
        super().__init__()
        self.args.add_required(name="Foo", default="f", validate=lambda user_data: user_data == "f",
                               help="Must be the letter f")
        self.args.add_required(name="Bar", default="aaaaa")
        self.args.add_required(name="Baz", default="aaaa")
        self.args.add_optional(name="Baz1")

    @property
    def title(self) -> str:
        return "Garbage Maker"


class MyScriptGUI(SimpleGui):
    def process(self):
        self.script.start()
        pass


def main():
    print("Hello ", __file__)
    script = MyScript()
    # script.run()
    # logger = logging.getLogger(__name__)
    # logger.setLevel(logging.DEBUG)
    # script.logger.setLevel(logging.INFO)
    script.logger.setLevel(logging.DEBUG)
    std_logger = logging.StreamHandler()
    debug_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    std_logger.setFormatter(debug_format)

    # logger.addHandler(std_logger)
    script.logger.addHandler(std_logger)
    app = SimpleGui(script)
    # app = MyScriptGUI(script)
    app.gui_logger.addHandler(std_logger)
    app.load_logger(debug=False)
    app.display()


if __name__ == '__main__':
    main()
