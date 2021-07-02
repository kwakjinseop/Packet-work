import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        w = QWidget()

        QToolTip.setFont(QFont('SaneSerif', 10))
        self.setToolTip('This is <b>Qwidget</b> a widget')
        btn=QPushButton('Send', self)
        btn.setToolTip("This is a <b>QPushButton</b>  widget")
        btn.resize(btn.sizeHint())
        btn.move(400,200)
        myTextbox = QLineEdit(w)
        myTextbox.move(50,50)
        myTextbox.resize(360, 40)


        self.setGeometry(300,300,300,300)
        self.setWindowTitle('ToolTips')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())

