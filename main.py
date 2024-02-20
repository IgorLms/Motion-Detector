import os
import sys

from PyQt5 import QtWidgets, QtGui

from window_app.app import App

basedir = os.path.dirname(__file__)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'data/logo.ico')))
    window = QtWidgets.QWidget()
    window.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'data/logo.ico')))
    a = App()
    a.show()
    sys.exit(app.exec_())
