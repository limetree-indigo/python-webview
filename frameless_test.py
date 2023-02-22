import sys

from PySide6.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel
from PySide6.QtCore import QTimer, Qt, QPoint




class Windows(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.resize(200, 200)
        self.show()

        self.btn = QPushButton("clcik", self)
        self.btn.resize(200, 200)
        self.setCentralWidget(self.btn)

    def mousePressEvent(self, event):
        # self.oldPos = event.globalPosition().toPoint()
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == Qt.LeftButton:
            self.__mousePressPos = event.globalPosition().toPoint()
            self.__mouseMovePos = event.globalPosition().toPoint()

        self.btn.mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        # self.move(self.x()+delta.x(), self.y()+delta.y())
        # self.oldPos = event.globalPosition().toPoint()
        if event.buttons() == Qt.LeftButton:
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPosition().toPoint()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)

            self.__mouseMovePos = globalPos
        self.btn.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            moved = event.globalPosition().toPoint - self.__mousePressPos
            if moved.manhattanLegth() > 3:
                event.ignore()
                return
            
        self.btn.mouseReleaseEvent(event)
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Windows()
    app.exec()