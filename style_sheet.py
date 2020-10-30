from PyQt5 import QtCore


def load_stylesheet():
    f = QtCore.QFile(f'style.qss')

    if not f.exists():
        return
    else:
        f.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        ts = QtCore.QTextStream(f)
        stylesheet = ts.readAll()
        return stylesheet
