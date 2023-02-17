import sys

import winsound # wav 파일 전용, 따로 패키지 설치할 필요없음

import requests
from pygame import mixer
from playsound import playsound
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QThread, QTimer
from PySide6.QtMultimedia import QMediaPlayer
import asyncio


mixer.init()
mixer.music.load("baemin_alert.wav")


class CallValue(QThread):
    def run(self):
        while True:
            self.sleep(3)
            print("call value")


class Form(QMainWindow):
    def __init__(self):
        self.url = ""
        QMainWindow.__init__(self)
        self.init_widget()

    
    def init_widget(self):
        self.setWindowTitle("QWebEngineView")
        self.web = QWebEngineView()
        self.web.load(QUrl("http://pos.handsorder.com/"))
        self.web.urlChanged.connect(self.changed_url)
        # self.web.loadProgress.connect(self.load_finish)
        self.setCentralWidget(self.web)
        # schedule.every(3).seconds.do(self.web.reload)
        self.web.loadFinished.connect(self.load_finish)
        

    def changed_url(self):
        self.url = self.web.url().toString()
        self.web.page().runJavaScript('localStorage.getItem("shop_cd");', 0, self.change_call_function)
        self.web.page().runJavaScript('localStorage.getItem("authorization");', 0, self.change_call_function)
        self.web.page().runJavaScript('document.querySelector(".flex_div>.posmenu_wr>a:first-child").innerText', 0, self.change_call_function)
        print("changed url:", self.url)
        if self.url == "http://pos.handsorder.com/#/shop_order_list":
            # call_value = CallValue()
            # call_value.start()
            self.timer = QTimer(self)
            self.timer.start(2000)
            self.timer.timeout.connect(self.test)

    def test(self):
        print("abc")
        # self.player = QMediaPlayer()
        # self.player.setSource(QUrl.fromLocalFile("/sound/notification.mpe"))
        # self.player.setVolume(50)
        # self.player.play()
        # playsound("./sound/notification.wav")
        mixer.music.play()
        # winsound.PlaySound("baemin_alert.wav", winsound.SND_FILENAME)
        # winsound.PlaySound("baemin_alert.wav", winsound.SND_FILENAME)
        


    def load_finish(self):
        script = """var req = new XMLHttpRequest();
        req.open('GET', document.location, false);
        req.send(null);
        var headers = req.getAllRequestHeaders().toLowerCase();
        headers;        
        """
        # self.web.page().runJavaScript(script, 0, self.call_function)
        self.web.page().runJavaScript('localStorage.getItem("shop_cd");', 0, self.load_finish_call_function)
        self.web.page().runJavaScript('localStorage.getItem("authorization");', 0, self.change_call_function)
        self.web.page().runJavaScript('document.querySelector(".flex_div>.posmenu_wr>a:first-child").innerText', 0, self.load_finish_call_function)
        # print("ok")

    def load_finish_call_function(self, val):
        print("load_finish:", val)

    def change_call_function(self, val):
        print("change:", val)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    # call_value = CallValue()
    # call_value.start()

    sys.exit(app.exec())
