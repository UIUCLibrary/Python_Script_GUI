import logging
import time
from PyQt5 import QtWidgets, QtGui

WAIT_TIME = 0.05
STICKY_THRESHOLD = 40

class QtLogger(logging.Handler):
    def __init__(self, widget: QtWidgets.QTextBrowser, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = widget
        self.last_called = time.time()

    def emit(self, record):
        delta_t = time.time() - self.last_called
        if delta_t < WAIT_TIME:
            time.sleep(WAIT_TIME - delta_t)
        msg = self.format(record)
        self.widget.append(str(msg))
        QtGui.QGuiApplication.processEvents()
        # TODO: Limit so it only flushes buffer

        sb = self.widget.verticalScrollBar()

        # keep text scrolled at the bottom as it updates if it's already at the bottom
        diff = sb.maximum() - sb.value()
        if diff < STICKY_THRESHOLD:
            sb.setValue(sb.maximum())
        self.last_called = time.time()