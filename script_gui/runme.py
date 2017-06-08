import contextlib
import logging
import random
import sys
import threading
from time import sleep

from PyQt5 import QtWidgets

import gui
# from .simple_gui import AbsSimpleGui
from gui_logger import QtLogger


class Worker(contextlib.AbstractContextManager):
    def __init__(self, callback):
        self.stopper = threading.Event()
        self._cb = callback
        self.t = threading.Thread()

    def __enter__(self):

        self.t = threading.Thread(target=self._cb, args=(self.stopper,))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)
        if self.t.is_alive():
            self.t.join()

    def start(self):
        if self.t:
            self.t.start()

    def stop(self):
        self.stopper.set()
        if self.t and self.t.is_alive():
            self.t.join()

    def reset(self):
        self.stopper.clear()
        self.t = threading.Thread(target=self._cb, args=(self.stopper,))


class Gui(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    thread = None

    @property
    def title(self):
        return "Garbage producer"

    def __init__(self, worker) -> None:
        super().__init__()

        # print(self.windowTitle())

        # self.window().setWindowTitle("ASDFASDFASDFASDFs")
        self.worker = worker
        self.setupUi(self)
        self.pushButton.clicked.connect(self.start)
        self.processing = False

    def start(self):

        if not self.processing:
            self.worker.start()
            self.processing = True
        else:
            self.worker.stop()
            self.processing = False
            self.worker.reset()

    def closeEvent(self, *args, **kwargs):
        self.worker.stop()
        super().closeEvent(*args, **kwargs)


def main():
    logger = logging.getLogger(__name__)

    logger.setLevel(logging.DEBUG)
    std_logger = logging.StreamHandler()
    std_logger.setLevel(logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv)
    with Worker(generate_garbage) as w:
        window = Gui(w)
        qt_logger = QtLogger(window.textBrowser)

        logger.addHandler(qt_logger)
        logger.addHandler(std_logger)
        window.setWindowTitle("fdasdasfadsf")

        window.show()
    app.exec_()


def generate_garbage(stopper):
    logger = logging.getLogger(__name__)
    while not stopper.is_set():
        text_block = "ASDFasdfasdfacviewnqwerf"
        a = random.randrange(1, len(text_block))
        b = "".join(random.sample(text_block, len(text_block)))
        logger.info("Sample message: Random text \"{}\"".format(b[0:a]))
        sleep(.1)


def my_excepthook(type, value, tback):
    # log the exception here

    # then call the default handler
    sys.__excepthook__(type, value, tback)


if __name__ == '__main__':
    sys.excepthook = my_excepthook
    main()
