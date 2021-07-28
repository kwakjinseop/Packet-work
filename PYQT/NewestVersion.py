import csv
import os
from os.path import dirname, realpath, join
import serial.tools.list_ports
import xlwt as xlwt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import serial, random, string, sys, secrets
from PyQt5 import QtWidgets, QtGui, QtCore, QtTest
import qdarkstyle
import collections
import pandas as pd
from PyQt5.uic import loadUiType
import pandas as pd
import serial.tools.list_ports



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
signal = ""

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
combomsg = ""
NumRows=0


linked_list = collections.deque()
txt = ""

From_Main, _ = loadUiType(join(dirname(__file__), "untitled.ui"))


class Ui_FilterView(QWidget, From_Main):
    def setupUi(self, FilterView):
        global Length_1, STX_O, CheckSum_O, Payload_O, combomsg

        FilterView.setWindowTitle("FilterView")
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

        self.tableWidget.setItem(0, 1, QTableWidgetItem((hex(packet[0]))))  # STX
        STX_O = str(hex(packet[0]))
        self.tableWidget.setItem(0, 2, QTableWidgetItem(str.join("", ("0x%02X " % i for i in packet[1:5]))))  # Time
        self.tableWidget.setItem(0, 3, QTableWidgetItem(str.join("", ("0x%02X " % i for i in packet[5:9]))))  # Checksum
        CheckSum_O = str.join("", ("0x%02X " % i for i in packet[5:9]))
        self.tableWidget.setItem(0, 4, QTableWidgetItem(str.join("", ("0x%02X " % i for i in packet[9:13]))))  # Reserved
        i = 14
        while (i < len(packet)):
            Length_1 += 1
            i += 1
        self.tableWidget.setItem(0, 5, QTableWidgetItem(str(Length_0)))  # Reserved
        self.tableWidget.setItem(0, 6, QTableWidgetItem(str.join("", ("0x%02X " % i for i in packet[15:]))))  # Payload
        Payload_O = sum(packet[15:])

        Length_1 = str.join("", ("0x%02X " % i for i in packet[15:]))

        self.tableWidget.setItem(0, 5, QTableWidgetItem(str.join("", ("0x%02X " % i for i in packet[14:]))))  # Payload
        self.model = QtGui.QStandardItemModel(FilterView)

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


        # 1번 그룹박스 생성
        self.groupbox1 = QtWidgets.QGroupBox(FilterView)
        self.groupbox1.setTitle("Network")
        self.groupbox1.setGeometry(QtCore.QRect(30, 770, 501, 221))
        self.portnamelabel = QtWidgets.QLabel(self.groupbox1)
        self.portnamelabel.setGeometry(QtCore.QRect(60, 50, 61, 51))
        self.portnamelabel.setText("Port :")
        self.portnamelabel.setScaledContents(False)
        self.portnamelabel.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.portnamelabel.setIndent(5)
        self.statuslabel = QtWidgets.QLabel(self.groupbox1)
        self.statuslabel.setGeometry(QtCore.QRect(50, 120, 61, 51))
        self.statuslabel.setText("Status :")
        self.statuslabel.setScaledContents(False)
        self.statuslabel.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.statuslabel.setIndent(5)
        self.conditionlabel = QtWidgets.QLabel(self.groupbox1)
        self.conditionlabel.setGeometry(QtCore.QRect(130, 120, 161, 51))
        self.conditionlabel.setText("Unknown")
        self.conditionlabel.setScaledContents(False)
        self.conditionlabel.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.conditionlabel.setIndent(5)
        self.conditionlabel.setObjectName("label_3")

        ports = serial.tools.list_ports.comports()
        a = [port.name for port in ports]
        self.comboBox2 = QtWidgets.QComboBox(self.groupbox1)
        self.comboBox2.setGeometry(QtCore.QRect(130, 50, 111, 51))
        for i in range(len(a)):
            self.comboBox2.addItem(a[i])
            combomsg=self.comboBox2.currentText()
        self.sendButton = QtWidgets.QPushButton(self.groupbox1)
        self.sendButton.setGeometry(QtCore.QRect(320, 20, 111, 101))
        self.sendButton.setText("Send")
        self.sendButton.clicked.connect(self.uart)
        self.pauseButton = QtWidgets.QPushButton(self.groupbox1)
        self.pauseButton.setGeometry(QtCore.QRect(260, 140, 91, 61))
        self.pauseButton.setText("Pause")
        self.pauseButton.clicked.connect(self.pause)
        self.stopButton = QtWidgets.QPushButton(self.groupbox1)
        self.stopButton.setGeometry(QtCore.QRect(380, 140, 91, 61))
        self.stopButton.setText("Stop")
        self.stopButton.clicked.connect(self.stop)

        # 2번 그룹박스 생성
        self.groupbox2 = QtWidgets.QGroupBox(FilterView)
        self.groupbox2.setTitle("Filter")
        self.groupbox2.setGeometry(QtCore.QRect(640, 770, 501, 221))
        self.comboBox = QtWidgets.QComboBox(self.groupbox2)
        self.comboBox.setGeometry(QtCore.QRect(30, 80, 111, 61))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("Number")
        self.comboBox.addItem("STX")
        self.comboBox.addItem("Time")
        self.comboBox.addItem("CheckSum")
        self.comboBox.addItem("Reserved")
        self.comboBox.addItem("Length")
        self.comboBox.addItem("Payload")
        self.comboBox.currentTextChanged.connect(self.combosubject)
        self.textEdit = QtWidgets.QTextEdit(self.groupbox2)
        self.textEdit.setGeometry(QtCore.QRect(160, 80, 211, 61))
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(self.groupbox2)
        self.pushButton.setGeometry(QtCore.QRect(380, 80, 91, 61))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Apply")
        self.pushButton.clicked.connect(self.filtering)

        # 3번 그룹박스 생성
        self.groupbox3 = QtWidgets.QGroupBox(FilterView)
        self.groupbox3.setTitle("View")
        self.groupbox3.setGeometry(QtCore.QRect(1220, 770, 501, 221))
        self.radioButton = QtWidgets.QRadioButton(self.groupbox3)
        self.radioButton.setText("Raw Data")
        self.radioButton.setGeometry(QtCore.QRect(30, 40, 141, 61))
        self.radioButton.setObjectName("radioButton")
        self.radioButton.clicked.connect(self.RawData)
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupbox3)
        self.radioButton_2.setText("Filtered Data")
        self.radioButton_2.setGeometry(QtCore.QRect(30, 130, 121, 51))
        self.radioButton_2.setObjectName("radioButton_2")

        # 4번 그룹박스 생성
        self.groupbox4 = QtWidgets.QGroupBox(self.groupbox3)
        self.groupbox4.setTitle("CSV")
        self.groupbox4.setGeometry(QtCore.QRect(190, 30, 271, 161))
        self.pushButton_3 = QtWidgets.QPushButton(self.groupbox4)
        self.pushButton_3.setGeometry(QtCore.QRect(150, 30, 91, 51))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText("Export")
        self.pushButton_3.clicked.connect(self.handleSavemon)
        self.pushButton_4 = QtWidgets.QPushButton(self.groupbox4)
        self.pushButton_4.setGeometry(QtCore.QRect(30, 30, 91, 51))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setText("Import")
        self.pushButton_4.clicked.connect(self.loadCsv)
        self.pushButton_5 = QtWidgets.QPushButton(self.groupbox4)
        self.pushButton_5.setGeometry(QtCore.QRect(90, 90, 91, 51))
        self.pushButton_5.setText("Describe")
        self.pushButton_5.clicked.connect(self.dataHead)

        FilterView.setCentralWidget(self.centralwidget)


    # def RawData(self):
    #     
    #

    def stop(self):
        global signal
        signal = "Stop"


    def pause(self):
        global signal
        # print("Paused")
        signal="Pause"

    def sleep(self,n):
        QtTest.QTest.qWait(n*1000)


    def uart(self):  # 20개의 패킷이 들어옴 //15부터 payload
        global value1
        global packet, combomsg, signal, NumRows
        global STX, CheckSum, Length, Time, checksum, Payload_O, leng, n_rows, start, Number, textPayload, textSTX, textTime, textCheckSum, textReserved, textLength, msg
        ser = serial.Serial(combomsg, 115200, timeout=1)
        ############랜덤 16진수 문자열 생성 부분##################
        print(NumRows)
        for NumRows in range(20000):
            if signal == "Pause":
                self.sleep(10)
                signal="normal"
            elif signal == "Stop":
                break
            else:
                self.sleep(0.5)

            key = secrets.token_hex(20)
            line_two = [" ".join(key[i:i + 2]) for i in range(0, len(key), 2)]
            answer = "0xab"
            for i in range(len(line_two)):
                sentences = line_two[i]
                sentences = ''.join(sentences.split())
                answer += " "+sentences  #answer가 완성된 랜덤 문장임.

            self.tableWidget.setRowCount(n_rows)
            self.tableWidget.scrollToBottom()

            op = answer
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
            self.sleep(0.1)



    def loadCsv(self):
        try:
            path = QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')[0]
            self.all_data = pd.read_csv(path)
        except:
            print(path)

    def dataHead(self):
        global NumRows, Number, value1
        NumRows = len(self.all_data.index)
        self.tableWidget.setRowCount(NumRows+value1+2)
        for i in range(-1,NumRows):
            for j in range(7):
                self.tableWidget.setItem(value1, j, QTableWidgetItem(str(self.all_data.iat[i, j])))
            value1 = value1 + 1


    def combosubject(self):
        global msg
        if (self.comboBox.currentText() == "Number"):
            msg = 0
        elif (self.comboBox.currentText() == "STX"):
            msg = 1
        elif (self.comboBox.currentText() == "Time"):
            msg = 2
        elif (self.comboBox.currentText() == "CheckSum"):
            msg = 3
        elif (self.comboBox.currentText() == "Reserved"):
            msg = 4
        elif (self.comboBox.currentText() == "Length"):
            msg = 5
        elif (self.comboBox.currentText() == "Payload"):
            msg = 6

    def filtering(self, fileName): #필터 버튼을 눌렀을 경우
        global msg, value2, txt, NumRows, value1
        global STX, CheckSum, Length, Time, checksum, Payload_O, leng, n_rows, start, Number, textPayload, textSTX, textTime, textCheckSum, textReserved, textLength, msg, TS, TR, TP, Reserved, Payload
        query = self.textEdit.toPlainText()
        self.filename = fileName

        if msg==0: #Number로 콤보박스를 체크했을 경우
                for i in range(0,value1):
                    data = self.tableWidget.item(i,0)
                    txt=data.text()
                    print(query+":"+txt)
                    if txt == query: #만약에 일치하는 경우
                        self.tableWidget_2.setItem(value2, 0, QTableWidgetItem(self.tableWidget.item(i, 0)))
                        self.tableWidget_2.setItem(value2, 1, QTableWidgetItem(self.tableWidget.item(i, 1)))
                        self.tableWidget_2.setItem(value2, 2, QTableWidgetItem(self.tableWidget.item(i, 2)))
                        self.tableWidget_2.setItem(value2, 3, QTableWidgetItem(self.tableWidget.item(i, 3)))
                        self.tableWidget_2.setItem(value2, 4, QTableWidgetItem(self.tableWidget.item(i, 4)))
                        self.tableWidget_2.setItem(value2, 5, QTableWidgetItem(self.tableWidget.item(i, 5)))
                        self.tableWidget_2.setItem(value2, 6, QTableWidgetItem(self.tableWidget.item(i, 6)))
                        value2 = value2 +1


        if msg==2: #Time로 콤보박스를 체크했을 경우
            for i in range(0,value1):
                data = self.tableWidget.item(i,2)
                txt=data.text()
                print(query + ":" + txt)
                if txt == query: #만약에 일치하는 경우
                    self.tableWidget_2.setItem(value2, 0, QTableWidgetItem(self.tableWidget.item(i, 0)))
                    self.tableWidget_2.setItem(value2, 1, QTableWidgetItem(self.tableWidget.item(i, 1)))
                    self.tableWidget_2.setItem(value2, 2, QTableWidgetItem(self.tableWidget.item(i, 2)))
                    self.tableWidget_2.setItem(value2, 3, QTableWidgetItem(self.tableWidget.item(i, 3)))
                    self.tableWidget_2.setItem(value2, 4, QTableWidgetItem(self.tableWidget.item(i, 4)))
                    self.tableWidget_2.setItem(value2, 5, QTableWidgetItem(self.tableWidget.item(i, 5)))
                    self.tableWidget_2.setItem(value2, 6, QTableWidgetItem(self.tableWidget.item(i, 6)))
                    value2 = value2 + 1

        if msg == 4:  # Reserved로 콤보박스를 체크했을 경우
            for i in range(0, value1):
                data = self.tableWidget.item(i, 4)
                txt = data.text()
                print(query+":"+txt)

                if txt == query:  # 만약에 일치하는 경우
                    self.tableWidget_2.setItem(value2, 0, QTableWidgetItem(self.tableWidget.item(i, 0)))
                    self.tableWidget_2.setItem(value2, 1, QTableWidgetItem(self.tableWidget.item(i, 1)))
                    self.tableWidget_2.setItem(value2, 2, QTableWidgetItem(self.tableWidget.item(i, 2)))
                    self.tableWidget_2.setItem(value2, 3, QTableWidgetItem(self.tableWidget.item(i, 3)))
                    self.tableWidget_2.setItem(value2, 4, QTableWidgetItem(self.tableWidget.item(i, 4)))
                    self.tableWidget_2.setItem(value2, 5, QTableWidgetItem(self.tableWidget.item(i, 5)))
                    self.tableWidget_2.setItem(value2, 6, QTableWidgetItem(self.tableWidget.item(i, 6)))
                    value2 = value2 + 1

        if msg == 5:  # Reserved로 콤보박스를 체크했을 경우
            for i in range(0,value1):
                data = self.tableWidget.item(i, 5)
                txt = data.text()
                print(query+":"+txt)
                if txt == query:  # 만약에 일치하는 경우

                    self.tableWidget_2.setItem(value2, 0, QTableWidgetItem(self.tableWidget.item(i, 0)))
                    self.tableWidget_2.setItem(value2, 1, QTableWidgetItem(self.tableWidget.item(i, 1)))
                    self.tableWidget_2.setItem(value2, 2, QTableWidgetItem(self.tableWidget.item(i, 2)))
                    self.tableWidget_2.setItem(value2, 3, QTableWidgetItem(self.tableWidget.item(i, 3)))
                    self.tableWidget_2.setItem(value2, 4, QTableWidgetItem(self.tableWidget.item(i, 4)))
                    self.tableWidget_2.setItem(value2, 5, QTableWidgetItem(self.tableWidget.item(i, 5)))
                    self.tableWidget_2.setItem(value2, 6, QTableWidgetItem(self.tableWidget.item(i, 6)))
                    value2 = value2 + 1

        if msg == 6:  # Payload로 콤보박스를 체크했을 경우
            for i in range(0, value1):
                data = self.tableWidget.item(i, 6)
                txt = data.text()
                print(query+":"+txt)

                if txt == query:  # 만약에 일치하는 경우

                    self.tableWidget_2.setItem(value2, 0, QTableWidgetItem(self.tableWidget.item(i, 0)))
                    self.tableWidget_2.setItem(value2, 1, QTableWidgetItem(self.tableWidget.item(i, 1)))
                    self.tableWidget_2.setItem(value2, 2, QTableWidgetItem(self.tableWidget.item(i, 2)))
                    self.tableWidget_2.setItem(value2, 3, QTableWidgetItem(self.tableWidget.item(i, 3)))
                    self.tableWidget_2.setItem(value2, 4, QTableWidgetItem(self.tableWidget.item(i, 4)))
                    self.tableWidget_2.setItem(value2, 5, QTableWidgetItem(self.tableWidget.item(i, 5)))
                    self.tableWidget_2.setItem(value2, 6, QTableWidgetItem(self.tableWidget.item(i, 6)))
                    value2 = value2 + 1

    def handleSavemon(self):
        #        with open('monschedule.csv', 'wb') as stream:
        with open('sampledata.csv', 'w') as stream:  # 'w'
            writer = csv.writer(stream, lineterminator='\n')  # + , lineterminator='\n'
            for row in range(self.tableWidget_2.rowCount()):
                rowdata=[]
                for column in range(self.tableWidget_2.columnCount()):
                    item = self.tableWidget_2.item(row, column)
                    if item is not None:
                        # rowdata.append(unicode(item.text()).encode('utf8'))
                        rowdata.append(item.text())  # +
                writer.writerow(rowdata)





class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter








if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FilterView = QtWidgets.QMainWindow()
    ui = Ui_FilterView()
    ui.setupUi(FilterView)
    FilterView.show()
    sys.exit(app.exec_())

