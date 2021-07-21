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


value1 = 0
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

STX_O = "0"  # default로 설정된 프로토콜 값
CheckSum_O = 0
Length_0 = 0
Length_1 = 0
Count = 0
n_rows = 2
start = 1
Number = 1

textPayload = []
textSTX = " "
textTime = []
textCheckSum = []
textReserved = []
textLength = []
msg = 0

TS = 0
TR = 0
TP = 0




class Background(QtWidgets.QMainWindow):
    command = QtCore.pyqtSignal(str)

    def __init__(self):  # 칼럼: 6, 로우: 20
        global STX_O, CheckSum_O, Length_0, checksum, Payload_O
        super().__init__()
        self.setWindowTitle("Background")
        n_cols = 7
        self.table = QTableWidget()
        self.table.setColumnCount(n_cols)
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        mw = QWidget()
        mw.setLayout(layout)
        self.setCentralWidget(mw)  # 오후 1시 44분

        self.te_query = QTextEdit(self)
        self.btn_button = QPushButton("Send", self)
        self.te_query.move(40, 850)
        self.btn_button.move(387, 850)
        self.btn_button.resize(100, 40)
        self.te_query.resize(300, 40)
        self.btn_button.clicked.connect(self.uart)

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
            "Reserved\n=======================\n" + str.join("", ("0x%02X " % i for i in packet[9:13]))))  # Reserved
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
        self.cb.addItem('All')
        self.cb.addItem('STX')
        self.cb.addItem('Time')
        self.cb.addItem('CheckSum')
        self.cb.addItem('Reserved')
        self.cb.addItem('Length')
        self.cb.addItem('Payload')
        self.cb.resize(100, 40)
        self.cb.move(940, 850)
        self.cb.currentTextChanged.connect(self.combobox_select)
        # self.th.start()
        # self.th1.start()
        self.show()

    def combobox_select(self):
        global start, msg
        # print(self.cb.currentText())  # 콤보박스 안에 값 출력
        if (self.cb.currentText() == "All"):
            msg = 0
        elif (self.cb.currentText() == "STX"):
            msg = 1
        elif (self.cb.currentText() == "Time"):
            msg = 2
        elif (self.cb.currentText() == "CheckSum"):
            msg = 3
        elif (self.cb.currentText() == "Reserved"):
            msg = 4
        elif (self.cb.currentText() == "Length"):
            msg = 5
        elif (self.cb.currentText() == "Payload"):
            msg = 6

    @QtCore.pyqtSlot()
    def uart(self):  # 20개의 패킷이 들어옴 //15부터 payload
        global value1
        global packet, Count
        global STX, CheckSum, Length, Time, checksum, Payload_O, leng, n_rows, start, Number, textPayload, textSTX, textTime, textCheckSum, textReserved, textLength, msg, TS, TR, TP
        self.table.setRowCount(n_rows)
        linked_list = collections.deque() #값을 담을 링크드리스트 생성
        query = self.te_query.toPlainText()
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

        linked_list.append(STX)
        linked_list.append(Time)
        linked_list.append(checksum)
        linked_list.append(Reserved)
        linked_list.append(str(Length))
        linked_list.append(Payload)


        self.table.setItem(value1, 0, QTableWidgetItem(str(Number)))
        self.table.setItem(value1, 1, QTableWidgetItem(linked_list[1]))  # STX
        self.table.setItem(value1, 2, QTableWidgetItem(linked_list[2]))  # Time
        self.table.setItem(value1, 3, QTableWidgetItem(linked_list[3]))  # Checksum
        self.table.setItem(value1, 4, QTableWidgetItem(linked_list[4]))  # Reserved
        self.table.setItem(value1, 5, QTableWidgetItem(linked_list[5]))  # Length
        self.table.setItem(value1, 6, QTableWidgetItem(linked_list[6]))  # Payload

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
        Count += 1
        n_rows += 1
        Number += 1

class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter

        # layout = QVBoxLayout
        # layout.addWidget(self.table)