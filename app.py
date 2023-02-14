import sys


from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QThread, QSize
from PySide6.QtWidgets import QApplication, QDialog, QMainWindow


class Worker(QThread):
    t = 0
    def run(self):
        while True:
            print("시간", self.t)
            self.sleep(5)
            self.t += 5

class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("hello")
        self.setFixedSize(QSize(150, 150))


class CreateDialog(QThread):
    def run(self):
        self.sleep(5)

        dlg = CustomDialog()
        dlg.exec()


class HansPos(QWebEngineView):
    def __init__(self):
        super().__init__()

        self.load(QUrl("http://pos.handsorder.com/"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HansPos()
    window.showMaximized()
    worker = Worker()
    worker.start()
    dlg = QDialog()
    dlg.setWindowTitle("test")
    dlg.exec()
    app.exec()