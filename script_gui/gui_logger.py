import logging

from PyQt5 import QtWidgets, QtGui


class QtLogger(logging.Handler):
    def __init__(self, widget: QtWidgets.QTextBrowser, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = widget

    def emit(self, record):
        msg = self.format(record)
        self.widget.append(str(msg))
        QtGui.QGuiApplication.processEvents()

        sb = self.widget.verticalScrollBar()

        # keep text scrolled at the bottom as it updates if it's already at the bottom
        diff = sb.maximum() - sb.value()
        if diff < 20:
            sb.setValue(sb.maximum())