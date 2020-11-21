from PyQt5.QtCore import pyqtSignal, QObject, QEvent


def clickable(widget):
    """
    Makes widget to be clickable.

    :param widget: QLabel to receive clicks
    :return: clickable widget
    """

    class Filter(QObject):
        clicked = pyqtSignal()

        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        return True
            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked
