import sys

from pygame import mixer   # 소리내기
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QTimer

mixer.init()
mixer.music.load("notification.wav")

class Form(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.init_widget()

    def init_widget(self):
        self.setWindowTitle("Hands App Order")
        self.web = QWebEngineView()
        self.web.load(QUrl("http://pos.handsorder.com/"))
        self.web.urlChanged.connect(self.change_url)
        self.setCentralWidget(self.web)

    def change_url(self):
        self.script = """
        var name = localStorage.getItem("name");
        var shop_cd = localStorage.getItem("shop_cd");
        name+":"+shop_cd;
        """
        self.web.page().runJavaScript(self.script, 0, self.change_call_function)

    def change_call_function(self, value):
        self.value = value.split(":")
        if "null" not in self.value:
            print(value)
            self.script = f"""
            var pro = document.querySelector(".order_state");
            pro.innerText = pro.innerText + '-' + '{value}';
            """
            self.web.page().runJavaScript(self.script)
            self.timer = QTimer(self)
            self.timer.start(2000)
            self.timer.timeout.connect(self.alert)
            

    def alert(self):
        print("주문")
        mixer.music.play()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()

    sys.exit(app.exec())
