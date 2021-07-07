import binascii

import PyQt5.QtWidgets as qtwid
import serial
import sys
import secrets
import random
import numpy as np
import time
from PyQt5 import QtWidgets, QtCore


value1 = 1
packet = [0xAB, 0x00, 0x00, 0x3C, 0x8C,  #STX, #Time
                  0x00, 0x00, 0x03, 0xA0,  # check digit
                  0xC0, 0xA8, 0xC9, 0x83,  # Reserved
                  0xC0, 0xA8, 0xC9, 0x80, 0xAF, 0x40, 0x00, # Payload
                  ]
STX = "True"
CheckSum = 0
Length = 0
Time = "0"
checksum = 0
Respond = "blank"


STX_O = "0" #default로 설정된 프로토콜 값
CheckSum_O = 0
Length_0 = 0

class MainWindow(qtwid.QMainWindow):

    def __init__(self):
        super().__init__()
        self.te_query = qtwid.QTextEdit(self) #문자열 입력부분
        self.btn_confirm = qtwid.QPushButton("확인",self)
        self.tableWidget = qtwid.QTableWidget(self)
        self.Initialize()

    def Initialize(self):
        self.setWindowTitle("PyQT")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(20)
        self.setGeometry(300, 100, 600, 400)
        self.tableWidget.resize(1000, 500)
        self.tableWidget.horizontalHeader().setSectionResizeMode(qtwid.QHeaderView.Stretch)
        self.setTableWidgetData()
        self.table = QtWidgets.QTableWidget()
        self.table.setSortingEnabled(True)

        self.te_query.move(10,510) #문자열 입력부분
        self.te_query.resize(300,40) #문자열 입력부분
        self.btn_confirm.move(330,510) #확인 버튼
        self.btn_confirm.resize(100,40) #확인버튼
        self.btn_confirm.clicked.connect(self.uart)

    def setTableWidgetData(self):
        global STX_O, CheckSum_O, Length_0, checksum
        column_headers = ['STX', 'Time', 'Checksum', 'Reserved', 'Length', 'Payload']

        self.tableWidget.setHorizontalHeaderLabels(column_headers)
        table = QtWidgets.QTableWidget()
        table.setSortingEnabled(True)

        self.tableWidget.setItem(0, 0, qtwid.QTableWidgetItem((hex(packet[0]))))  # STX
        STX_O = str(hex(packet[0]))
        self.tableWidget.setItem(0, 1, qtwid.QTableWidgetItem(str.join("",("0x%02X " % i for i in packet[1:5]))))  # Time
        self.tableWidget.setItem(0, 2, qtwid.QTableWidgetItem(str.join("",("0x%02X " % i for i in packet[6:9]))))  # Checksum
        CheckSum_O = str.join("",("0x%02X " % i for i in packet[6:9]))
        self.tableWidget.setItem(0, 3, qtwid.QTableWidgetItem(str.join("",("0x%02X " % i for i in packet[10:14])))) # Respond
        self.tableWidget.setItem(0, 4, qtwid.QTableWidgetItem(str.join("",("0x%02X " % i for i in packet[15:])))) # Length


        j=0
        hexidemal = 0
        while (j<len(packet)):
            hexidemal =
        Length_0 = str.join("",("0x%02X " % i for i in packet[15:]))


        self.tableWidget.setItem(0, 5, qtwid.QTableWidgetItem(str.join("",("0x%02X " % i for i in packet[14:]))))  # Payload


    def uart(self): #20개의 패킷이 들어옴 //15부터 payload
        global value1
        global packet
        global STX, CheckSum, Length, Time, checksum
        query = self.te_query.toPlainText()
        ser = serial.Serial("COM3", 115200, timeout=1)
        op = query
        a = op.split(" ")
        # print(type(a[15]))
        print(a[15])
        i=15
        while(i<len(a)):
            CheckSum += int(a[i],16)
            print(CheckSum)
            i+=1

        xx= hex(CheckSum)
        print(xx) #0x238출력
        print(checksum)

        j=15
        if(a[0]==STX_O): #완벽하게 일치한 패킷이 들어왔을 경우
            STX = "True"
            Time = " ".join(a[1:5])
            while(j<len(a)):
                Length +=1
                j+=1
            Reserved = " ".join(a[10:14])
            Payload = " ".join(a[15:])

        self.tableWidget.setItem(value1, 0, qtwid.QTableWidgetItem(STX)) #STX
        self.tableWidget.setItem(value1, 1, qtwid.QTableWidgetItem(Time)) #Time
        # self.tableWidget.setItem(value1, 2, qtwid.QTableWidgetItem(str(op.split(':')[2]))) #Checksum
        self.tableWidget.setItem(value1, 3, qtwid.QTableWidgetItem(Reserved)) #Respond
        self.tableWidget.setItem(value1, 4, qtwid.QTableWidgetItem(str(Length))) #Length
        self.tableWidget.setItem(value1, 5, qtwid.QTableWidgetItem(Payload)) #Payload

        value1=value1+1
        if op is 'q':
            ser.close()


    def on_comboBox_currentIndexChanged(self, index):
        self.proxy.setFilterKeyColumn(index)

    def on_lineEdit_textChanged(self, text):
        search = QtCore.QRegExp(text,
                                QtCore.Qt.CaseInsensitive,
                                QtCore.QRegExp.RegExp
                                )

        self.proxy.setFilterRegExp(search)

    def on_signalMapper_mapped(self, i):
        stringAction = self.signalMapper.mapping(i).text()
        filterColumn = self.logicalIndex
        filterString = QtCore.QRegExp(stringAction,
                                      QtCore.Qt.CaseSensitive,
                                      QtCore.QRegExp.FixedString
                                      )

        self.proxy.setFilterRegExp(filterString)
        self.proxy.setFilterKeyColumn(filterColumn)

    def on_actionAll_triggered(self):
        filterColumn = self.logicalIndex
        filterString = QtCore.QRegExp("",
                                      QtCore.Qt.CaseInsensitive,
                                      QtCore.QRegExp.RegExp
                                      )

        self.proxy.setFilterRegExp(filterString)
        self.proxy.setFilterKeyColumn(filterColumn)







if __name__ == "__main__":
    app = qtwid.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    app.exec()