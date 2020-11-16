from PyQt5 import QtCore


def load_stylesheet():
    """
    Loads style.qss content

    :return: style sheet for :class:`messenger.MessengerWindow`
    :rtype: str
    """

    style = QtCore.QFile(f'style.qss')

    if not style.exists():
        return
    else:
        style.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        text = QtCore.QTextStream(style)
        stylesheet = text.readAll()
        return stylesheet
