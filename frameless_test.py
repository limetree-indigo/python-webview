import sys

from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import QTimer, Qt, QPoint


class Windows(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.resize(200, 200)
        self.show()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x()+delta.x(), self.y()+delta.y())
        self.oldPos = event.globalPos()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Windows()
    app.exec()