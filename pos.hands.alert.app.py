import sys

import requests
from pygame import mixer   # 소리내기
from PySide6.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QTimer, Signal, Slot, QPoint, Qt

mixer.init()
mixer.music.load("notification.wav")

class PopUp(QWidget):
    on_top = Signal()

    def __init__(self):
        super().__init__()

        # 창이 뜰 때 최상단에 위치
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.setFixedSize(200, 200)

        self.btn = QPushButton("주문", self)
        self.btn.resize(200, 200)
        self.btn.clicked.connect(self.run)

    # def mousePressEvent(self, event):
    #     self.oldPos = event.globalPos()
    #     print(self.oldPos)

    # def mouseMoveEvent(self, event):
    #     delta = QPoint(event.globalPos() - self.oldPos)
    #     self.move(self.x() + delta.x(), self.y() + delta.y())
    #     self.oldPos = event.globalPos()
    
    @Slot()
    def run(self):
        self.on_top.emit()


class Form(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.init_widget()

    # 메인 화면 초기화
    def init_widget(self):
        self.setWindowTitle("Hands App Order")
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.web = QWebEngineView()
        self.web.load(QUrl("http://pos.handsorder.com/"))
        self.web.urlChanged.connect(self.change_url)
        self.setCentralWidget(self.web)

    # url이 변경될 때 localStorge에 있는 값을 가져온다.
    def change_url(self):
        self.script = """
        var name = localStorage.getItem("authorization");
        var shop_cd = localStorage.getItem("shop_cd");
        name+" "+shop_cd;
        """
        self.web.page().runJavaScript(self.script, 0, self.change_call_function)

    # localStorage 에 값이 있다면 10초에 한번씩 api를 요청한다.
    def change_call_function(self, value):
        self.value = value.split()
        if "null" not in self.value:
            self.timer = QTimer(self)
            self.timer.start(5000)
            self.timer.timeout.connect(self.call_api)

    # localStorage 에 값에 따라 주문대기가 있는지 확인한다.
    # 주문대기가 있으면 소리와 함께 알림창을 띄운다.
    def call_api(self):
        url = "https://app.handsnetwork.com/rest_free/pos/getPosChk"
        token, shop_cd = self.value
        headers = {"authorization": token}
        res = requests.get(url, headers=headers, params={"shop_cd": shop_cd})
        self.cnt = eval(res.text)['cnt']
        if self.cnt > 0:
            print("주문")
            self.web.reload()
            mixer.music.play()
            self.pop_up = PopUp()
            self.pop_up.btn.setText(f"주문 : {self.cnt}")
            self.pop_up.on_top.connect(self.go_top)
            self.pop_up.show()

    # 알림창 버튼을 클릭했을 때 알림창은 닫히고 주문창이 최상단으로 온다.
    def go_top(self):
        print("go_top")
        self.pop_up.close()
        self.showNormal()
        self.activateWindow()

    # 주문 창이 닫히면 알림창도 같이 닫힌다.
    def closeEvent(self, event):
        self.pop_up.close()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())
