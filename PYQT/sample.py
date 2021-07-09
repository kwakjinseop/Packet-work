import xlwt as xlwt
from PyQt5.QtGui import QBrush, QFont, QPixmap, QColor
from PyQt5.QtWidgets import *
import serial, random, string, sys, secrets
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, QtGui
import threading, time
import qdarkstyle
import csv
from PyQt5 import QtCore


import sys

value1 = 1
packet = [0xAB, 0x00, 0x00, 0x3C, 0x8C,  #STX, #Time
                  0x00, 0x00, 0x03, 0xA0,  # check digit
                  0xC0, 0xA8, 0xC9, 0x83,  # Reserved
                  0xC0, 0xA8, 0xC9, 0x80, 0xAF, 0x40, 0x00, # Payload
                  ]


STX = "True"
CheckSum = 0
Length = 0
leng = 0
Time = "0"
Respond = "blank"
Payload_O = 0
checksum =""

STX_O = "0" #default로 설정된 프로토콜 값
CheckSum_O = 0
Length_0 = 0

class MainWindow(QMainWindow):
    def __init__(self): #칼럼: 6, 로우: 20
        global STX_O, CheckSum_O, Length_0, checksum, Payload_O
        super().__init__()


        self.comboxbutton = QPushButton("Select")

        # self.comboxbutton.clicked.connect(combo)
        self.query = QLineEdit()
        self.query.setPlaceholderText("Search...")
        # combo = QComboBox(mw)
        # combo.addItems(['STX', 'Time', 'Checksum', 'Reserved', 'Length', 'Payload' ])
        # combo.move(20,70)
        self.query.textChanged.connect(self.search)

        n_rows = 20
        n_cols = 6
        self.table = QTableWidget()
        self.table.setRowCount(n_rows)
        self.table.setColumnCount(n_cols)


        layout = QVBoxLayout()

        layout.addWidget(self.query)
        layout.addWidget(self.table)

        mw = QWidget()
        mw.setLayout(layout)
        self.setCentralWidget(mw)

        self.te_query = QTextEdit(self)
        self.btn_button = QPushButton("Send", self)
        self.te_query.move(40,850)
        self.btn_button.move(387, 850)
        self.btn_button.resize(100,40)
        self.te_query.resize(300,40)
        self.btn4 = QPushButton("Add Column", self)
        self.btn4.move(500,850)
        self.btn4.resize(100,40)
        self.btn_button.clicked.connect(self.uart)
        self.btn4.clicked.connect(self.__btn4_clicked)
        # self.btn_button.clicked.connect(self.cellbackgroundcolor())

        self.btn6 = QPushButton("Delete Column", self)
        self.btn6.move(610, 850)
        self.btn6.resize(100,40)
        self.btn6.clicked.connect(self.__btn6_clicked)

        self.btn7 = QPushButton("Add Row", self)
        self.btn7.move(720, 850)
        self.btn7.resize(100, 40)
        self.btn7.clicked.connect(self.__btn7_clicked)

        self.btn9 = QPushButton("Delete Row", self)
        self.btn9.move(830, 850)
        self.btn9.resize(100,40)
        self.btn9.clicked.connect(self.__btn9_clicked)




        self.table.setSortingEnabled(True)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        column_headers = ['STX', 'Time', 'Checksum', 'Reserved', 'Length', 'Payload']
        self.table.setHorizontalHeaderLabels(column_headers)

        self.table.setItem(0, 0, QTableWidgetItem("STX\n========\n"+(hex(packet[0]))))  # STX
        STX_O = str(hex(packet[0]))
        self.table.setItem(0, 1, QTableWidgetItem("Time\n=======================\n"+str.join("", ("0x%02X " % i for i in packet[1:5]))))  # Time
        self.table.setItem(0, 2, QTableWidgetItem("Checksum\n=======================\n"+str.join("", ("0x%02X " % i for i in packet[5:9]))))  # Checksum
        CheckSum_O = str.join("", ("0x%02X " % i for i in packet[5:9]))
        self.table.setItem(0, 3, QTableWidgetItem("Reserved\n=======================\n"+str.join("", ("0x%02X " % i for i in packet[9:13]))))  # Reserved
        i=14
        while (i<len(packet)):
            Length_0+=1
            i+=1
        self.table.setItem(0, 4, QTableWidgetItem("Length\n========\n"+str(Length_0))) # Reserved
        self.table.setItem(0, 5, QTableWidgetItem(str.join("", ("0x%02X " % i for i in packet[15:]))))  # Payload
        Payload_O = sum(packet[15:])


        Length_0 = str.join("", ("0x%02X " % i for i in packet[15:]))

        self.table.setItem(0, 5, QTableWidgetItem("Payload\n=======================\n"+str.join("", ("0x%02X " % i for i in packet[14:]))))  # Payload

        delegate = AlignDelegate(self.table)
        self.table.setItemDelegateForColumn(0, delegate)
        self.table.setItemDelegateForColumn(1, delegate)
        self.table.setItemDelegateForColumn(2, delegate)
        self.table.setItemDelegateForColumn(3, delegate)
        self.table.setItemDelegateForColumn(4, delegate)
        self.table.setItemDelegateForColumn(5, delegate)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)











    def search(self, s): # 검색기능 함수
        items = self.table.findItems(s, Qt.MatchContains)
        if items:
            item = items[0]
            self.table.setCurrentItem(item)


    def uart(self):  # 20개의 패킷이 들어옴 //15부터 payload
        global value1
        global packet
        global STX, CheckSum, Length, Time, checksum, Payload_O, leng
        query = self.te_query.toPlainText()
        ser = serial.Serial("COM3", 115200, timeout=1)
        op = query
        a = op.split(" ")
        if(a == "q"):
            ser.close()

        # print(type(a[15]))
        i = 15
        while (i < len(a)):
            CheckSum += int(a[i], 16)
            i += 1
        print(CheckSum)

        print(Payload_O)

        j = 15
        if (a[0] == STX_O):  # 완벽하게 일치한 패킷이 들어왔을 경우
            STX = "True"
            Time = " ".join(a[1:5])
            if (CheckSum == Payload_O):
                checksum = "Pass"
            else:
                checksum = "Fail"
            while (j < len(a)):
                leng += 1
                Length = leng
                j += 1
            leng = 0
            print(Length)
            Reserved = " ".join(a[10:14])
            Payload = " ".join(a[15:])
        else:
            STX = "False"
            Time = "False"
            checksum = "False"
            Reserved = "False"
            Payload = "False"
            Length = "False"

        self.table.setItem(value1, 0, QTableWidgetItem("STX\n========\n"+STX))  # STX
        self.table.setItem(value1, 1, QTableWidgetItem("Time\n=======================\n"+Time))  # Time
        self.table.setItem(value1, 2, QTableWidgetItem("Checksum\n=======================\n"+checksum))  # Checksum
        self.table.setItem(value1, 3, QTableWidgetItem("Reserved\n=======================\n"+   Reserved))  # Respond
        self.table.setItem(value1, 4, QTableWidgetItem("Length\n========\n"+str(Length)))  # Length
        self.table.setItem(value1, 5, QTableWidgetItem("Payload\n=======================\n"+Payload))  # Payload

        delegate = AlignDelegate(self.table)
        self.table.setItemDelegateForColumn(0, delegate)
        self.table.setItemDelegateForColumn(1, delegate)
        self.table.setItemDelegateForColumn(2, delegate)
        self.table.setItemDelegateForColumn(3, delegate)
        self.table.setItemDelegateForColumn(4, delegate)
        self.table.setItemDelegateForColumn(5, delegate)

        value1 = value1 + 1
        CheckSum = 0


    def DebugChecking(str):
        cnt = 0
        while(cnt<10):
            time.sleep(random.randint(0, 100) / 300.0)
            print(str, cnt)
            cnt += 1
            print("=== ", str, "스레드 종료 ===")

    def Threading(count):
        print("uart로 통신시작")
        count.uart()

    def __btn4_clicked(self):
        col_count = self.table.columnCount()
        self.table .setColumnCount(col_count+1)

    def __btn6_clicked(self):
        self.table.removeColumn(1)  # column 삭제

    def __btn7_clicked(self):
        row_count = self.table.rowCount()
        self.table.setRowCount(row_count + 1)  # row 추가

    def __btn9_clicked(self):
        self.table.removeRow(1)  # 1번째 row 삭제

    cnt = threading.Thread(target = Threading, args=(1,))


    # def cellbackgroundcolor(self):
    #     x = random.randint(1, 3)  # 1 <= x <= 3  사이의 임의의 수
    #     myitem = self.table.item(0, 0)
    #     if x == 1:
    #         myitem.Background(QBrush(QPixmap("exit.png")))  # cell 배경
    #     elif x == 2:
    #         myitem.Background(QtGui.Qcolor('red'))
    #
    #     else:
    #         myitem.Background(QBrush(QColor(0, 255, 0)))
    #
    #     return


    # cnt2 = threading.Thread(target= DebugChecking, args=("체크용",))
    # print("===Thread Operating===")
    # cnt.start()
    # cnt2.start()
    #
    # cnt2.join()
    # print("체크종료")
    def savefile(self):
        filename = Unicode(QtGui.QFileDialog.getSaveFileName(self, 'Save File', '', ".xls(*.xls)"))
        wbk = xlwt.Workbook()
        self.sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
        self.add2()
        wbk.save(filename)

    def add2(self):
        row = 0
        col = 0
        for i in range(self.tableWidget.columnCount()):
            for x in range(self.tableWidget.rowCount()):
                try:
                    teext = str(self.tableWidget.item(row, col).text())
                    self.sheet.write(row, col, teext)
                    row += 1
                except AttributeError:
                    row += 1
            row = 0
            col += 1

class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter


if __name__ == "__main__":
    app = QApplication([])
    mw = QtWidgets.QMainWindow()

    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # or in new API
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))


    mw = MainWindow()
    mw.show()

    app.exec()