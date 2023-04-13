import sys
from PyQt6.QtWidgets import QApplication
from window import WindowApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WindowApp()
    window.show()

    app.exec()
