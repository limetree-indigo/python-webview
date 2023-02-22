import sys

import requests
import re
from pygame import mixer
from PySide6.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QTimer, Qt, QSize, QEvent
from PySide6.QtGui import QIcon, QScreen

# mixer.init()
# mixer.music.load("notification.wav")
class CallOrderList(QWidget):
    def __init__(self):
        super().__init__()

        self.i_size = 120
        # 배경투명하게, 최상단으로
        self.setWindowFlag(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.btn = QPushButton("", self)
        self.btn.setIcon(QIcon("order_wait.png"))
        self.btn.setIconSize(QSize(self.i_size, self.i_size))
        self.btn.resize(self.i_size, self.i_size)        
        self.btn.setStyleSheet("background:transparent")
        self.center()

    def center(self):
        screen = QScreen.availableSize(QApplication.primaryScreen())
        framx = (screen.width()-self.i_size)/2
        framy = (screen.height()-self.i_size)/2
        self.btn.move(framx, framy)

class Form(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        self.init_widget()
        self.setFixedSize(640, 480)

    def init_widget(self):
        self.setWindowTitle("Hands App Order")

        self.web = QWebEngineView()
        self.web.load(QUrl("http://pos.handsorder.com/"))
        self.web.urlChanged.connect(self.change_url)
        self.setCentralWidget(self.web)

    # url이 변경될 때 localStorge에 있는 값을 가져온다.
    def change_url(self):
        script = """
        var name = localStorage.getItem("authorization");
        var shop_cd = localStorage.getItem("shop_cd");
        name+" "+shop_cd;
        """
        self.web.page().runJavaScript(script, 0, self.change_call_function)

    # localStorage 에 값이 있다면 10초에 한번씩 api를 요청한다.
    # localStorage 에 값이 있다면 버튼 화면 띄움
    def change_call_function(self, value):
        self.value = value.split()
        if "null" not in self.value:
            self.call_orderlist = CallOrderList()
            self.call_orderlist.showMaximized()
            self.call_orderlist.btn.clicked.connect(self.show_orderlist)
            self.timer = QTimer(self)
            self.timer.start(5000)
            self.timer.timeout.connect(self.call_api)

    def show_orderlist(self):
        print("go orderlist")
        self.showNormal()
        self.activateWindow()

     # localStorage 에 값에 따라 주문대기가 있는지 확인한다.
    # 주문대기가 있으면 소리와 함께 주문 페이지로 가는 버튼을 알림버튼으로 변경한다.
    def call_api(self):
        url = "https://app.handsnetwork.com/rest_free/pos/getPosChk"
        token, shop_cd = self.value
        headers = {"authorization": token}
        res = requests.get(url, headers=headers, params={"shop_cd": shop_cd})
        self.cnt = eval(res.text)['cnt']
        # self.cnt = 1
        if self.cnt > 0:
            print("주문")
            self.call_orderlist.btn.setIcon(QIcon("order_alert.png"))
            self.web.reload()
            # mixer.music.play()
        else:
            self.call_orderlist.btn.setIcon(QIcon("order_wait.png"))    

    # 주문 페이지가 최소화될 때, 주문 대기에 해당하는 태그의 텍스트 값을 is_wait 함수의 매개변수로 넘겨준다.
    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                # print("changeEvent: 최소화 실행")
                script = """
                var wait = document.querySelector(".posmenu_wr>a:first-child");
                var wait_value = wait ? wait.innerText : "";
                wait_value;
                """
                self.web.page().runJavaScript(script, 0, self.is_wait)
            # elif self.windowState() & Qt.WindowMaximized:
            #     print("changeEvent : 최대화 실행")
            # elif event.oldState():
            #     print("changeEvent : 원래 화면복구")    

    # 주문 대기가 없으면 주문페이지로 가는 버튼을 기본버튼으로 변경한다.
    # 주문 대기가 있으면 주문페이지로 가는 버튼을 알림버튼으로 변경한다.
    def is_wait(self, value):
        if value:
            # print(value)
            number = int(re.sub(r"[^0-9]", '', value))
            if number > 0:
                self.call_orderlist.btn.setIcon(QIcon("order_alert.png"))
            else:
                self.call_orderlist.btn.setIcon(QIcon("order_wait.png"))
    
    def closeEvent(self, event):
        self.call_orderlist.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())