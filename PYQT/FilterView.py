import xlwt as xlwt
from PyQt5.QtGui import QBrush, QFont, QPixmap, QColor
from PyQt5.QtWidgets import *
import serial, random, string, sys, secrets
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, QtGui, QtCore
import multiprocessing as mp
import qdarkstyle
from threading import Thread
import collections
import pandas as pd




value1 = 0
value2 = 0
packet = [0xAB, 0x00, 0x00, 0x3C, 0x8C,  # STX, #Time
          0x00, 0x00, 0x03, 0xA0,  # check digit
          0xC0, 0xA8, 0xC9, 0x83,  # Reserved
          0xC0, 0xA8, 0xC9, 0x80, 0xAF, 0x40, 0x00,  # Payload
          ]

STX = "True"
CheckSum = 0
Length = 0
leng = 0
Time = "0"
Respond = "blank"
Payload_O = 0
checksum = ""
Reserved = ""
Payload = ""

STX_O = "0"  # default로 설정된 프로토콜 값
CheckSum_O = 0
Length_0 = 0
Length_1 = 0
Count = 0
n_rows = 1
start = 1
Number = 1

textPayload = []
textSTX = " "
textTime = []
textCheckSum = []
textReserved = []
textLength = []
msg = -1


result=""
linked_list = collections.deque()
txt = ""

class Ui_FilterView(object):
    def setupUi(self, FilterView):
        global Length_1, STX_O, CheckSum_O, Payload_O
        FilterView.setWindowTitle("FilterView")
        FilterView.setObjectName("FilterView")
        FilterView.resize(1912, 951)
        FilterView.setStyleSheet("Grid layout")
        self.centralwidget = QtWidgets.QWidget(FilterView)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 10, 881, 751))
        self.tableWidget.setRowCount(20000)
        self.tableWidget.setColumnCount(7)
        column_headers = ['Number', 'STX', 'Time', 'Checksum', 'Reserved', 'Length', 'Payload']
        self.tableWidget.setHorizontalHeaderLabels(column_headers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setSortingEnabled(True)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        column_headers = ['Number', 'STX', 'Time', 'Checksum', 'Reserved', 'Length', 'Payload']
        self.tableWidget.setHorizontalHeaderLabels(column_headers)

        self.tableWidget.setItem(0, 1, QTableWidgetItem("STX\n=======================\n" + (hex(packet[0]))))  # STX
        STX_O = str(hex(packet[0]))
        self.tableWidget.setItem(0, 2, QTableWidgetItem(
            "Time\n=======================\n" + str.join("", ("0x%02X " % i for i in packet[1:5]))))  # Time
        self.tableWidget.setItem(0, 3, QTableWidgetItem(
            "Checksum\n=======================\n" + str.join("", ("0x%02X " % i for i in packet[5:9]))))  # Checksum
        CheckSum_O = str.join("", ("0x%02X " % i for i in packet[5:9]))
        self.tableWidget.setItem(0, 4, QTableWidgetItem(
            "Reserved\n=======================\n" + str.join("", ("0x%02X " % i for i in packet[9:13]))))  # Reserved
        i = 14
        while (i < len(packet)):
            Length_1 += 1
            i += 1
        self.tableWidget.setItem(0, 5, QTableWidgetItem("Length\n=======================\n" + str(Length_0)))  # Reserved
        self.tableWidget.setItem(0, 6, QTableWidgetItem(str.join("", ("0x%02X " % i for i in packet[15:]))))  # Payload
        Payload_O = sum(packet[15:])

        Length_1 = str.join("", ("0x%02X " % i for i in packet[15:]))

        self.tableWidget.setItem(0, 5, QTableWidgetItem(
            "Payload\n=======================\n" + str.join("", ("0x%02X " % i for i in packet[14:]))))  # Payload

        #############왼쪽 테이블########################
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(890, 300, 91, 41))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("Number")
        self.comboBox.addItem("STX")
        self.comboBox.addItem("Time")
        self.comboBox.addItem("CheckSum")
        self.comboBox.addItem("Reserved")
        self.comboBox.addItem("Length")
        self.comboBox.addItem("Payload")
        self.comboBox.currentTextChanged.connect(self.combosubject)
        #############콤보박스##############################

        self.tableWidget_2 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_2.setGeometry(QtCore.QRect(990, 10, 891, 751))
        self.tableWidget_2.setRowCount(20000)
        self.tableWidget_2.setColumnCount(7)
        self.tableWidget_2.setObjectName("tableWidget_2")
        column_headers = ['Number', 'STX', 'Time', 'Checksum', 'Reserved', 'Length', 'Payload']
        self.tableWidget_2.setHorizontalHeaderLabels(column_headers)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSortingEnabled(True)
        #############오른쪽 테이블##########################
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(890, 350, 91, 41))
        self.textEdit.setObjectName("textEdit")
        #############텍스트 입력상자#########################
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(890, 400, 91, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Apply")
        self.pushButton.clicked.connect(self.filtering)
        #############Apply 버튼###########################
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(10, 770, 321, 51))
        self.textEdit_2.setObjectName("textEdit_2")
        #############텍스트 입력상자#########################
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(340, 770, 111, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("Send")
        FilterView.setCentralWidget(self.centralwidget)
        self.pushButton_2.clicked.connect(self.uart)
        #############텍스트 전송버튼#########################
        self.pushCSV = QtWidgets.QPushButton(self.centralwidget)
        self.pushCSV.setGeometry(QtCore.QRect(890, 450, 91, 51))
        self.pushCSV.setObjectName("pushButton")
        self.pushCSV.setText("CSV")
        self.pushCSV.clicked.connect(self.csv)
        #############CSV 메뉴바#########################


    def uart(self):  # 20개의 패킷이 들어옴 //15부터 payload
        global value1
        global packet
        global STX, CheckSum, Length, Time, checksum, Payload_O, leng, n_rows, start, Number, textPayload, textSTX, textTime, textCheckSum, textReserved, textLength, msg
        self.tableWidget.setRowCount(n_rows)
        query = self.textEdit_2.toPlainText()
        ser = serial.Serial("COM3", 115200, timeout=1)
        op = query
        a = op.split(" ")

        if (a == "q"):
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



        self.tableWidget.setItem(value1, 0, QTableWidgetItem(str(Number)))
        self.tableWidget.setItem(value1, 1, QTableWidgetItem(STX))  # STX
        self.tableWidget.setItem(value1, 2, QTableWidgetItem(Time))  # Time
        self.tableWidget.setItem(value1, 3, QTableWidgetItem(checksum))  # Checksum
        self.tableWidget.setItem(value1, 4, QTableWidgetItem(Reserved))  # Reserved
        self.tableWidget.setItem(value1, 5, QTableWidgetItem(str(Length)))  # Length
        self.tableWidget.setItem(value1, 6, QTableWidgetItem(Payload))  # Payload


        delegate = AlignDelegate(self.tableWidget)
        self.tableWidget.setItemDelegateForColumn(0, delegate)
        self.tableWidget.setItemDelegateForColumn(1, delegate)
        self.tableWidget.setItemDelegateForColumn(2, delegate)
        self.tableWidget.setItemDelegateForColumn(3, delegate)
        self.tableWidget.setItemDelegateForColumn(4, delegate)
        self.tableWidget.setItemDelegateForColumn(5, delegate)

        self.tableWidget.verticalHeader().setDefaultSectionSize(120)

        value1 = value1 + 1
        CheckSum = 0
        n_rows += 1
        Number += 1



    def combosubject(self):
        global msg
        if (self.comboBox.currentText() == "Number"):
            print(self.comboBox.currentText())
            msg = 0
        elif (self.comboBox.currentText() == "STX"):
            print(self.comboBox.currentText())
            msg = 1
        elif (self.comboBox.currentText() == "Time"):
            print(self.comboBox.currentText())
            msg = 2
        elif (self.comboBox.currentText() == "CheckSum"):
            print(self.comboBox.currentText())
            msg = 3
        elif (self.comboBox.currentText() == "Reserved"):
            print(self.comboBox.currentText())
            msg = 4
        elif (self.comboBox.currentText() == "Length"):
            print(self.comboBox.currentText())
            msg = 5
        elif (self.comboBox.currentText() == "Payload"):
            print(self.comboBox.currentText())
            msg = 6

    def filtering(self): #필터 버튼을 눌렀을 경우
        global result, msg, value2, txt
        global STX, CheckSum, Length, Time, checksum, Payload_O, leng, n_rows, start, Number, textPayload, textSTX, textTime, textCheckSum, textReserved, textLength, msg, TS, TR, TP, Reserved, Payload
        query = self.textEdit.toPlainText()
        if msg==0: #Number로 콤보박스를 체크했을 경우
            for i in range(0,n_rows-1):
                data = self.tableWidget.item(i,0)
                txt=data.text()
                print(txt)
                if txt == query: #만약에 일치하는 경우
                    print("Yes")
                    self.tableWidget_2.setItem(value2, 0, QTableWidgetItem(self.tableWidget.item(i, 0)))
                    self.tableWidget_2.setItem(value2, 1, QTableWidgetItem(self.tableWidget.item(i, 1)))
                    self.tableWidget_2.setItem(value2, 2, QTableWidgetItem(self.tableWidget.item(i, 2)))
                    self.tableWidget_2.setItem(value2, 3, QTableWidgetItem(self.tableWidget.item(i, 3)))
                    self.tableWidget_2.setItem(value2, 4, QTableWidgetItem(self.tableWidget.item(i, 4)))
                    self.tableWidget_2.setItem(value2, 5, QTableWidgetItem(self.tableWidget.item(i, 5)))
                    self.tableWidget_2.setItem(value2, 6, QTableWidgetItem(self.tableWidget.item(i, 6)))
                    value2 = value2 +1
        if msg==2: #Time로 콤보박스를 체크했을 경우
            for i in range(0,n_rows-1):
                data = self.tableWidget.item(i,2)
                txt=data.text()
                print(txt)
                if txt == query: #만약에 일치하는 경우
                    print("Yes")
                    self.tableWidget_2.setItem(value2, 0, QTableWidgetItem(self.tableWidget.item(i, 0)))
                    self.tableWidget_2.setItem(value2, 1, QTableWidgetItem(self.tableWidget.item(i,1)))
                    self.tableWidget_2.setItem(value2, 2, QTableWidgetItem(self.tableWidget.item(i, 2)))
                    self.tableWidget_2.setItem(value2, 3, QTableWidgetItem(self.tableWidget.item(i, 3)))
                    self.tableWidget_2.setItem(value2, 4, QTableWidgetItem(self.tableWidget.item(i, 4)))
                    self.tableWidget_2.setItem(value2, 5, QTableWidgetItem(self.tableWidget.item(i, 5)))
                    self.tableWidget_2.setItem(value2, 6, QTableWidgetItem(self.tableWidget.item(i, 6)))
                    value2 = value2 + 1

        if msg == 4:  # Reserved로 콤보박스를 체크했을 경우
            for i in range(0, n_rows -1):
                data = self.tableWidget.item(i, 4)
                txt = data.text()
                print(txt)
                if txt == query:  # 만약에 일치하는 경우
                    print("Yes")
                    self.tableWidget_2.setItem(value2, 0, QTableWidgetItem(self.tableWidget.item(i, 0)))
                    self.tableWidget_2.setItem(value2, 1, QTableWidgetItem(self.tableWidget.item(i, 1)))
                    self.tableWidget_2.setItem(value2, 2, QTableWidgetItem(self.tableWidget.item(i, 2)))
                    self.tableWidget_2.setItem(value2, 3, QTableWidgetItem(self.tableWidget.item(i, 3)))
                    self.tableWidget_2.setItem(value2, 4, QTableWidgetItem(self.tableWidget.item(i, 4)))
                    self.tableWidget_2.setItem(value2, 5, QTableWidgetItem(self.tableWidget.item(i, 5)))
                    self.tableWidget_2.setItem(value2, 6, QTableWidgetItem(self.tableWidget.item(i, 6)))
                    value2 = value2 + 1

        if msg == 6:  # Payload로 콤보박스를 체크했을 경우
            for i in range(0, n_rows - 1):
                data = self.tableWidget.item(i, 6)
                txt = data.text()
                print(txt)
                if txt == query:  # 만약에 일치하는 경우
                    print("Yes")
                    self.tableWidget_2.setItem(value2, 0, QTableWidgetItem(self.tableWidget.item(i, 0)))
                    self.tableWidget_2.setItem(value2, 1, QTableWidgetItem(self.tableWidget.item(i, 1)))
                    self.tableWidget_2.setItem(value2, 2, QTableWidgetItem(self.tableWidget.item(i, 2)))
                    self.tableWidget_2.setItem(value2, 3, QTableWidgetItem(self.tableWidget.item(i, 3)))
                    self.tableWidget_2.setItem(value2, 4, QTableWidgetItem(self.tableWidget.item(i, 4)))
                    self.tableWidget_2.setItem(value2, 5, QTableWidgetItem(self.tableWidget.item(i, 5)))
                    self.tableWidget_2.setItem(value2, 6, QTableWidgetItem(self.tableWidget.item(i, 6)))
                    value2 = value2 + 1

    def csv(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', ".xls(*.xls)")
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.bold = True
        style.font = font
        model = self.tableWidget_2.model()
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

        # layout = QVBoxLayout
        # layout.addWidget(self.table)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FilterView = QtWidgets.QMainWindow()
    ui = Ui_FilterView()
    ui.setupUi(FilterView)
    FilterView.show()
    sys.exit(app.exec_())

