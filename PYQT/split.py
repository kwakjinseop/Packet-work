import sys

from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

__author__ = "Deokyu Lim <hong18s@gmail.com>"


class Form(QWidget):
    """
    만들고자 하는 프로그램의 기본이 되는 창 또는 폼 위젯.
    본 위젯 위에 다른 위젯을 올려서 모양을 만든다.
    QWidget을 상속받아서 필요한 메소드를 작성.
    """

    def __init__(self):
        """
        보통 __init__ (생성자)에서 필요한 것들을 다를 위젯들을 선언해줘도 되지만 init_widget을 따로 만들어서 호출한다.
        """
        QWidget.__init__(self, flags=Qt.Widget)

        self.te_1 = QTableWidget()
        self.te_1.setRowCount(20)
        self.te_1.setColumnCount(1)

        self.te_3 = QTextEdit() #텍스트 입력부분
        self.btn = QPushButton('Send', self) #버튼

        for i in range (20):
            for value in range(1):
                self.te_1.setItem(i, value, QTableWidgetItem(str(i+value)))
        self.te_1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # 표작성부분


        self.split_1 = QSplitter()
        self.split_2 = QSplitter()

        self.vbox = QVBoxLayout()
        self.container_vbox = QVBoxLayout()
        self.init_widget()

    def init_widget(self):
        """
        현재 위젯의 모양등을 초기화
        """
        self.setWindowTitle("Hello World")
        self.split_1.addWidget(self.te_1)
        self.container_vbox.addWidget(self.split_1)

        self.split_2.setOrientation(Qt.Vertical)
        self.split_2.addWidget(self.split_1)
        self.split_2.addWidget(self.te_3)


        self.vbox.addWidget(self.split_2)
        self.setLayout(self.vbox)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    exit(app.exec_())