import sys
from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5 import uic

form_class = uic.loadUiType(r'C:\Users\Geoplan\Desktop\곽진섭_인턴\design.ui')[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.click_button)

    def click_button(self):
        exist_textEdit = self.textEdit.text()
        self.textEdit.setText(exist_textEdit+self.pushButton.text())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec()
