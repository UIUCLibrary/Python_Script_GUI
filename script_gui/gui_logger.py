import logging

from PyQt5 import QtWidgets


class QtLogger(logging.Handler):
    def __init__(self, widget: QtWidgets.QTextBrowser, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = widget

    def emit(self, record):
        print("emitting")

        print("16")
        msg = self.format(record)
        print("18")
        print(msg)
        print(self.widget)
        self.widget.append(str(msg))
        print("21")
        sb = self.widget.verticalScrollBar()
        print("23")

        # keep text scrolled at the bottom as it updates if it's already at the bottom
        diff = sb.maximum() - sb.value()
        print("27")
        if diff < 20:
            sb.setValue(sb.maximum())
        print("30")
        print("emitted")