import xlwt as xlwt
from PyQt5.QtGui import QBrush, QFont, QPixmap, QColor
from PyQt5.QtWidgets import *
import serial, random, string, sys, secrets
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, QtGui, QtCore
import threading, time
import qdarkstyle
import csv, sys
import pandas as pd


import sys

value1 = 0
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
Count = 0
n_rows = 2
start = 0
model = 0
Number = 1


class MainWindow(QMainWindow):
    def __init__(self): #칼럼: 6, 로우: 20
        global STX_O, CheckSum_O, Length_0, checksum, Payload_O
        super().__init__()
        self.setWindowTitle("Background")


        self.comboxbutton = QPushButton("Select")

        # self.comboxbutton.clicked.connect(combo)
        self.query = QLineEdit()
        self.query.setPlaceholderText("Search...")

        self.query.textChanged.connect(self.search)

        n_cols = 7
        self.table = QTableWidget()

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
        column_headers = ['Number','STX', 'Time', 'Checksum', 'Reserved', 'Length', 'Payload']
        self.table.setHorizontalHeaderLabels(column_headers)

        self.table.setItem(0, 1, QTableWidgetItem("STX\n=======================\n"+(hex(packet[0]))))  # STX
        STX_O = str(hex(packet[0]))
        self.table.setItem(0, 2, QTableWidgetItem("Time\n=======================\n"+str.join("", ("0x%02X " % i for i in packet[1:5]))))  # Time
        self.table.setItem(0, 3, QTableWidgetItem("Checksum\n=======================\n"+str.join("", ("0x%02X " % i for i in packet[5:9]))))  # Checksum
        CheckSum_O = str.join("", ("0x%02X " % i for i in packet[5:9]))
        self.table.setItem(0, 4, QTableWidgetItem("Reserved\n=======================\n"+str.join("", ("0x%02X " % i for i in packet[9:13]))))  # Reserved
        i=14
        while (i<len(packet)):
            Length_0+=1
            i+=1
        self.table.setItem(0, 5, QTableWidgetItem("Length\n=======================\n"+str(Length_0))) # Reserved
        self.table.setItem(0, 6, QTableWidgetItem(str.join("", ("0x%02X " % i for i in packet[15:]))))  # Payload
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

        self.cb = QComboBox(self)
        self.cb.addItem('STX')
        self.cb.addItem('Time')
        self.cb.addItem('Checksum')
        self.cb.addItem('Reserved')
        self.cb.addItem('Length')
        self.cb.addItem('Payload')
        self.cb.resize(100, 40)
        self.cb.move(940, 850)
        self.cb.currentTextChanged.connect(self.combobox_select)
        self.change_color = QPushButton("Color On", self)
        self.change_color.clicked.connect(self.changecolor)
        self.change_color.resize(100, 40)
        self.change_color.move(1050, 850)

        self.buttonSave = QPushButton('Save', self)
        self.buttonSave.resize(100, 40)
        self.buttonSave.move(1160, 850)
        self.buttonSave.clicked.connect(self.SaveasExcel)
        self.display()

        def display(self):
            self.w = NewWindow()

class NewWindow(QtWidgets.QWidget):
    def __init__(self):
        global STX_O, CheckSum_O, Length_0, checksum, Payload_O
        super().__init__()
        self.setWindowTitle("Background")

        self.comboxbutton = QPushButton("Select")

            # self.comboxbutton.clicked.connect(combo)
        self.query = QLineEdit()
        self.query.setPlaceholderText("Search...")

        self.query.textChanged.connect(self.search)

        n_cols = 7
        self.table = QTableWidget()

        self.table.setColumnCount(n_cols)

        layout = QVBoxLayout()

        layout.addWidget(self.query)
        layout.addWidget(self.table)

        mw = QWidget()
        mw.setLayout(layout)
        self.setCentralWidget(mw)

        self.te_query = QTextEdit(self)
        self.btn_button = QPushButton("Send", self)
        self.te_query.move(40, 850)
        self.btn_button.move(387, 850)
        self.btn_button.resize(100, 40)
        self.te_query.resize(300, 40)
        self.btn4 = QPushButton("Add Column", self)
        self.btn4.move(500, 850)
        self.btn4.resize(100, 40)
        self.btn_button.clicked.connect(self.uart)
        self.btn4.clicked.connect(self.__btn4_clicked)
            # self.btn_button.clicked.connect(self.cellbackgroundcolor())

        self.btn6 = QPushButton("Delete Column", self)
        self.btn6.move(610, 850)
        self.btn6.resize(100, 40)
        self.btn6.clicked.connect(self.__btn6_clicked)

        self.btn7 = QPushButton("Add Row", self)
        self.btn7.move(720, 850)
        self.btn7.resize(100, 40)
        self.btn7.clicked.connect(self.__btn7_clicked)

        self.btn9 = QPushButton("Delete Row", self)
        self.btn9.move(830, 850)
        self.btn9.resize(100, 40)
        self.btn9.clicked.connect(self.__btn9_clicked)

        self.table.setSortingEnabled(True)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        column_headers = ['Number', 'STX', 'Time', 'Checksum', 'Reserved', 'Length', 'Payload']
        self.table.setHorizontalHeaderLabels(column_headers)

        self.table.setItem(0, 1, QTableWidgetItem("STX\n=======================\n" + (hex(packet[0]))))  # STX
        STX_O = str(hex(packet[0]))
        self.table.setItem(0, 2, QTableWidgetItem(
            "Time\n=======================\n" + str.join("", ("0x%02X " % i for i in packet[1:5]))))  # Time
        self.table.setItem(0, 3, QTableWidgetItem(
            "Checksum\n=======================\n" + str.join("", ("0x%02X " % i for i in packet[5:9]))))  # Checksum
        CheckSum_O = str.join("", ("0x%02X " % i for i in packet[5:9]))
        self.table.setItem(0, 4, QTableWidgetItem(
            "Reserved\n=======================\n" + str.join("",
                                                                 ("0x%02X " % i for i in packet[9:13]))))  # Reserved
        i = 14
        while (i < len(packet)):
            Length_0 += 1
            i += 1
            self.table.setItem(0, 5, QTableWidgetItem("Length\n=======================\n" + str(Length_0)))  # Reserved
            self.table.setItem(0, 6, QTableWidgetItem(str.join("", ("0x%02X " % i for i in packet[15:]))))  # Payload
            Payload_O = sum(packet[15:])

            Length_0 = str.join("", ("0x%02X " % i for i in packet[15:]))

            self.table.setItem(0, 5, QTableWidgetItem(
                "Payload\n=======================\n" + str.join("", ("0x%02X " % i for i in packet[14:]))))  # Payload

            delegate = AlignDelegate(self.table)
            self.table.setItemDelegateForColumn(0, delegate)
            self.table.setItemDelegateForColumn(1, delegate)
            self.table.setItemDelegateForColumn(2, delegate)
            self.table.setItemDelegateForColumn(3, delegate)
            self.table.setItemDelegateForColumn(4, delegate)
            self.table.setItemDelegateForColumn(5, delegate)

            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

            self.cb = QComboBox(self)
            self.cb.addItem('STX')
            self.cb.addItem('Time')
            self.cb.addItem('Checksum')
            self.cb.addItem('Reserved')
            self.cb.addItem('Length')
            self.cb.addItem('Payload')
            self.cb.resize(100, 40)
            self.cb.move(940, 850)
            self.cb.currentTextChanged.connect(self.combobox_select)
            self.change_color = QPushButton("Color On", self)
            self.change_color.clicked.connect(self.changecolor)
            self.change_color.resize(100, 40)
            self.change_color.move(1050, 850)

            self.buttonSave = QPushButton('Save', self)
            self.buttonSave.resize(100, 40)
            self.buttonSave.move(1160, 850)
            self.buttonSave.clicked.connect(self.SaveasExcel)
            self.display()





    def changecolor(self):
        for x in range(0,Count+1):
            self.table.item(x,0).setBackground(QBrush(Qt.darkGreen)) #아이템이 있어야지만 색깔이 칠해짐
            self.table.item(x, 1).setBackground(QBrush(Qt.darkYellow))
            self.table.item(x, 2).setBackground(QBrush(Qt.gray))
            self.table.item(x, 3).setBackground(QBrush(Qt.darkBlue))
            self.table.item(x, 4).setBackground(QBrush(Qt.darkRed))
            self.table.item(x, 5).setBackground(QBrush(Qt.darkCyan))


        # self.table.item(0,0).setBackground(QBrush(Qt.red))
        # for x in (1,20):
        #     myitem.setBackground(QBrush(Qt.red))
        #     # x+=1



    def combobox_select(self):
        print(self.cb.currentText()) #콤보박스 안에 값 출력





    def search(self, s): # 검색기능 함수
        items = self.table.findItems(s, Qt.MatchContains)
        if items:
            item = items[0]
            self.table.setCurrentItem(item)




    def uart(self):  # 20개의 패킷이 들어옴 //15부터 payload

        global value1
        global packet, Count
        global STX, CheckSum, Length, Time, checksum, Payload_O, leng, n_rows, start, Number
        self.table.setRowCount(n_rows)
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

            Reserved = " ".join(a[10:14])
            Payload = " ".join(a[15:])
        else:
            STX = "False"
            Time = "False"
            checksum = "False"
            Reserved = "False"
            Payload = "False"
            Length = "False"

        self.table.setItem(value1, 0, QTableWidgetItem(str(Number)))
        self.table.setItem(value1, 1, QTableWidgetItem(STX))  # STX
        self.table.setItem(value1, 2, QTableWidgetItem(Time))  # Time
        self.table.setItem(value1, 3, QTableWidgetItem(checksum))  # Checksum
        self.table.setItem(value1, 4, QTableWidgetItem(Reserved))  # Respond
        self.table.setItem(value1, 5, QTableWidgetItem(str(Length)))  # Length
        self.table.setItem(value1, 6, QTableWidgetItem(Payload))  # Payload

        delegate = AlignDelegate(self.table)
        self.table.setItemDelegateForColumn(0, delegate)
        self.table.setItemDelegateForColumn(1, delegate)
        self.table.setItemDelegateForColumn(2, delegate)
        self.table.setItemDelegateForColumn(3, delegate)
        self.table.setItemDelegateForColumn(4, delegate)
        self.table.setItemDelegateForColumn(5, delegate)

        self.table.verticalHeader().setDefaultSectionSize(120)

        value1 = value1 + 1
        CheckSum = 0
        Count+=1
        n_rows+=1
        Number+=1

        # model = self.table.model()
        #
        #
        # for start in range(n_rows):
        #     text = model.data(model.index(start, 1))
        #     start += 1
        #     print(start)
        #     print(text)






    # def DebugChecking(str):
    #     cnt = 0
    #     while(cnt<10):
    #         time.sleep(random.randint(0, 100) / 300.0)
    #         print(str, cnt)
    #         cnt += 1
    #         print("=== ", str, "스레드 종료 ===")
    #
    # def Threading(count):
    #     print("uart로 통신시작")
    #     count.uart()

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

    def SaveasExcel(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', ".xls(*.xls)")
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.bold = True
        style.font = font
        model = self.table.model()
        for c in range(model.columnCount()):
            text = model.headerData(c, QtCore.Qt.Horizontal)
            sheet.write(0, c + 1, text, style=style)

        for r in range(model.rowCount()):
            text = model.headerData(r, QtCore.Qt.Vertical)
            sheet.write(r + 1, 0, text, style=style)

        for c in range(model.columnCount()):
            for r in range(model.rowCount()):
                text = model.data(model.index(r, c))
                sheet.write(r + 1, c + 1, text)
        wbk.save(filename)




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