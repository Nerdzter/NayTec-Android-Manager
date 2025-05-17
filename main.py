import sys
from PyQt5.QtWidgets import QApplication
from view.MainWindow import MainWindow

def load_stylesheet():
    with open("resources/styles/theme.qss", "r") as f:
        return f.read()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet())

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
