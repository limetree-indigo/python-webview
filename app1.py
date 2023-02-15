import sys

from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl


class Form(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.init_widget()

    
    def init_widget(self):
        self.setWindowTitle("QWebEngineView")
        self.web = QWebEngineView()
        self.web.load(QUrl("http://pos.handsorder.com/"))
        self.web.urlChanged.connect(self.changed_url)
        # self.web.loadProgress.connect(self.load_finish)
        self.web.loadFinished.connect(self.load_finish)
        self.setCentralWidget(self.web)

    def changed_url(self):
        url = self.web.url().toString()
        print(url)

    def load_finish(self):
        script = """var req = new XMLHttpRequest();
        req.open('GET', document.location, false);
        req.send(null);
        var headers = req.getAllRequestHeaders().toLowerCase();
        headers;        
        """
        self.web.page().runJavaScript(script, 0, self.call_function)
        self.web.page().runJavaScript('localStorage.getItem("shop_cd");', 1, self.call_function)
        print("ok")

    def call_function(self, html):
        print(html)
        # print(type(html))
        # header = html.split('\r\n')
        # print(header)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    exit(app.exec())
