import logging
import time

import sys
from PyQt5 import QtWidgets, QtGui, QtCore
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
        self._send_it(record)
        self.last_called = time.time()

    def _send_it(self, record):


        msg = self.format(record)
        self.widget.append(str(msg))

        QtGui.QGuiApplication.processEvents()
        # TODO: Limit so it only flushes buffer

        sb = self.widget.verticalScrollBar()

        # keep text scrolled at the bottom as it updates if it's already at the bottom
        diff = sb.maximum() - sb.value()
        if diff < STICKY_THRESHOLD:
            self.widget.ensureCursorVisible()
            sb.setValue(sb.maximum())
            # curser = self.widget.textCursor()
            # assert isinstance(curser, QtGui.QTextCursor)
            # curser.setPosition(end)

            # f.movePosition(QtGui.QTextCursor.End)
            # print(f)
            # self.widget.setTextCursor(f)
