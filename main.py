from PyQt5.QtWidgets import QApplication
from window_app.app import App
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())
