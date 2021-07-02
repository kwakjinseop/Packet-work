import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SaneSerif', 10))

        self.setGeometry(500,500,500,200)
        self.setWindowIcon("images/letter-s.png")
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())

