import sys

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QSize, QUrl
from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.clicked.connect(self.button_clicked)

        self.setCentralWidget(button)

    def button_clicked(self):
        print("clicked")

app = QApplication(sys.argv)

# window = MainWindow()
window = QWebEngineView()
window.load(QUrl("http://pos.handsorder.com/"))
# window.load(QUrl("https://naver.com"))
# window.show()
window.showMaximized()



app.exec()