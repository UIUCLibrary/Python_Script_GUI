import logging

from PyQt5 import QtWidgets


class QtLogger(logging.Handler):
    def __init__(self, widget: QtWidgets.QTextBrowser, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = widget

    def emit(self, record):
        msg = self.format(record)
        self.widget.append(msg)
        sb = self.widget.verticalScrollBar()
        sb.setValue(sb.maximum() + 1)