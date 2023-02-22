import sys
from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow
from PySide6.QtCore import Qt


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.setStyleSheet("background:transparent")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.btn = QPushButton("click", self)
        self.btn.clicked.connect(self.run)

    def run(self):
        print("run")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.showMaximized()
    app.exec()