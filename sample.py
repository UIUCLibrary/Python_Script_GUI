import logging
import random
import threading
from time import sleep

from script_gui import SimpleGui, AbsScript


# import script_gui


class MyScript(AbsScript):
    def _script(self):
        # logger = logging.getLogger(__name__)
        while not self._abort_flag.is_set():
            print(len(self.args))
            for k,v in self.args.items():
                print(k ,v.value, v.valid)
            text_block = "ASDFasdfasdfacviewnqwerf"
            a = random.randrange(1, len(text_block))
            b = "".join(random.sample(text_block, len(text_block)))
            # logger.info("Sample message: Random text \"{}\"".format(b[0:a]))
            self.logger.info("Sample message: Random text \"{}\"".format(b[0:a]))
            sleep(.5)
        self.announce_ended()

    def run(self):
        self._script()

    def start(self):
        self.t = threading.Thread(target=self._script, daemon=True)
        self.t.start()

    def __init__(self):
        super().__init__()
        self.args.add_required(name="Foo", validate=lambda user_data: user_data == "f")
        self.args.add_required(name="Bar", default="aaaaa")
        self.args.add_required(name="Baz")



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
