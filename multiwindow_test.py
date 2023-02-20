import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Text", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.resize(300, 100)
        self.display()
        self.show()
    
    def display(self):
        self.w = NewWindow()
        self.w.command.connect(self.anyfunction)
    
    def closeEvent(self, event):
        self.w.close()

    @Slot(str)
    def anyfunction(self, msg):
        self.label.setText(msg)

class NewWindow(QWidget):
    command = Signal(str)
    def __init__(self):
        super().__init__()
        self.inputbox = QLineEdit(self)
        self.inputbox.resize(500, 100)
        self.inputbox.returnPressed.connect(self.sendCommand)
        self.show()

    @Slot()
    def sendCommand(self):
        msg = self.inputbox.text()
        self.command.emit(msg)
        self.inputbox.setText("")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())