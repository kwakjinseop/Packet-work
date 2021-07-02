import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *


class MyApp(QWidget):
    """표를 보여주는 위젯"""
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(20)
        self.tableWidget.setColumnCount(1)



        # 셀 내용 채우기
        for i in range (20):
            for value in range(1):
                self.tableWidget.setItem(i, value, QTableWidgetItem(str(i+value)))

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        self.setWindowTitle('PyQt5')
        self.setGeometry(300,100,600,400)
        self.show()

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())