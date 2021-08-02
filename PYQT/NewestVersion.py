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
import collections, threading
import pandas as pd
from PyQt5.uic import loadUiType
import pandas as pd
import serial.tools.list_ports


answer = ""
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
answer=""

STX_O = "0"  # default로 설정된 프로토콜 값
CheckSum_O = 0
Length_0 = 0
Length_1 = 0
Count = 0
n_rows = 1
start = 1
Number = 1
somethingvalue=""

line_two=""

msg = -1
combomsg = ""
NumRows=0

table1status = 0
table2status = 0


linked_list = collections.deque()
txt = ""

From_Main, _ = loadUiType(join(dirname(__file__), "untitled.ui"))



class Ui_FilterView(QWidget, From_Main):
    command = QtCore.pyqtSignal(str)

    def setupUi(self, FilterView):
        global Length_1, STX_O, CheckSum_O, Payload_O, somethingvalue
        FilterView.setWindowTitle("FilterView")
        FilterView.resize(1950, 980)
        FilterView.setStyleSheet("Grid layout")
        self.centralwidget = QtWidgets.QWidget(FilterView)
        self.centralwidget.setObjectName("centralwidget")
        self.model = QtGui.QStandardItemModel(FilterView)

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
        self.conditionlabel.setText(somethingvalue) # 여기서 이제 값이 connected/unconnected로 나뉠것임.
        self.conditionlabel.setScaledContents(False)
        self.conditionlabel.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.conditionlabel.setIndent(5)
        self.conditionlabel.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.groupbox1)
        self.pushButton.setGeometry(QtCore.QRect(10, 160, 93, 51))
        self.pushButton.setText("Connect")
        self.pushButton.clicked.connect(self.tryConnecting)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupbox1)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 160, 93, 51))
        self.pushButton_2.setText("Unconnect")
        self.pushButton_2.clicked.connect(QCoreApplication.instance().quit)


        # ports = serial.tools.list_ports.comports()
        # a = [port.name for port in ports]
        self.comboBox2 = QtWidgets.QComboBox(self.groupbox1)
        self.comboBox2.setGeometry(QtCore.QRect(130, 50, 111, 51))
        self.comboBox2.addItem("COM1")
        self.comboBox2.addItem("COM2")
        self.comboBox2.addItem("COM3")
        self.comboBox2.addItem("COM4")
        self.comboBox2.addItem("COM5")
        self.comboBox2.addItem("COM6")
        self.comboBox2.addItem("COM7")

        self.comboBox2.currentTextChanged.connect(self.comboBoxFunction)
        # for i in range(len(a)):
        #     self.comboBox2.addItem(a[i])
        #     combomsg=self.comboBox2.currentText()
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
        self.radioButton_2.clicked.connect(self.table2show)

        # 4번 그룹박스 생성
        self.groupbox4 = QtWidgets.QGroupBox(self.groupbox3)
        self.groupbox4.setTitle("CSV")
        self.groupbox4.setGeometry(QtCore.QRect(190, 30, 271, 161))
        self.pushButton_3 = QtWidgets.QPushButton(self.groupbox4)
        self.pushButton_3.setGeometry(QtCore.QRect(150, 30, 91, 51))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText("Export")
        self.pushButton_3.clicked.connect(self.writeCsv)
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

    def comboBoxFunction(self):
        global msg, answer
        if (self.comboBox2.currentText() == "COM1"):
            answer = "COM1"
        elif (self.comboBox2.currentText() == "COM2"):
            answer = "COM2"
        elif (self.comboBox2.currentText() == "COM3"):
            answer = "COM3"
        elif (self.comboBox2.currentText() == "COM4"):
            answer = "COM4"
        elif (self.comboBox2.currentText() == "COM5"):
            answer = "COM5"
        elif (self.comboBox2.currentText() == "COM6"):
            answer = "COM6"
        elif (self.comboBox2.currentText() == "COM7"):
            answer = "COM7"


    def tryConnecting(self,event):
        global answer, combomsg
        ports = serial.tools.list_ports.comports()
        a = [port.name for port in ports]
        print(a[0])
        if answer == a[0]:
            combomsg = answer
            self.setGeometry(300, 300, 300, 200)
            reply = QMessageBox.question(self, 'Message', 'Sucessfully Connected',
                                         QMessageBox.Yes )
        else:
            self.setGeometry(300, 300, 300, 200)
            reply = QMessageBox.question(self, 'Message', 'Try another port',
                                         QMessageBox.Yes)





    def uart(self):  # 20개의 패킷이 들어옴 //15부터 payload
        global value1, line_two, table2status, table1status
        global packet, combomsg, signal, NumRows
        global STX, CheckSum, Length, Time, checksum, Payload_O, leng, n_rows, start, Number, msg, Payload

        ser = serial.Serial(combomsg, 115200, timeout=1)

        ############랜덤 16진수 문자열 생성 부분##################
        entire=[]
        for NumRows in range(20000):

            key = secrets.token_hex(20)
            line_two = [" ".join(key[i:i + 2]) for i in range(0, len(key), 2)]
            answer = "0xab"
            for i in range(len(line_two)):
                sentences = line_two[i]
                sentences = ''.join(sentences.split())
                answer += " "+sentences  #answer가 완성된 랜덤 문장임.
            # try:
            entire.append(answer)
            # print(str(entire))

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 20, 2000, 741))
        self.tableWidget.setRowCount(20000)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setObjectName("tableWidget")
        column_headers = ['Number', 'STX', 'Time', 'Checksum', 'Reserved', 'Length', 'Payload']
        self.tableWidget.setHorizontalHeaderLabels(column_headers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSortingEnabled(True)

        global Length_1, STX_O, CheckSum_O, Payload_O, table1status, table2status
        self.tableWidget_2 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_2.setGeometry(QtCore.QRect(0, 20, 2000, 741))
        self.tableWidget_2.setRowCount(20000)
        self.tableWidget_2.setColumnCount(7)
        self.tableWidget_2.setObjectName("tableWidget_2")
        column_headers = ['Filtered Number', 'STX', 'Time', 'Checksum', 'Reserved', 'Length', 'Payload']
        self.tableWidget_2.setHorizontalHeaderLabels(column_headers)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        for i in range(0, 100):
            if signal == "Pause":
                self.sleep(10)
                signal="normal"
            elif signal == "Stop":
                break

            # self.sleep(1)
            self.tableWidget.setRowCount(n_rows)
            self.tableWidget.scrollToBottom()

            op = entire[i]
            a = op.split(" ")
            # print(a)

            # print(type(a[15]))
            i = 15
            while (i < len(a)):
                CheckSum += int(a[i], 16)
                i += 1

            j = 15
            if (a[0] == '0xab'):  # 완벽하게 일치한 패킷이 들어왔을 경우
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
            self.sleep(0.5)
            self.tableWidget.show()


    def RawData(self):
        global Length_1, STX_O, CheckSum_O, Payload_O, table1status, table2status
        self.tableWidget.setSortingEnabled(True)

        if (table2status == 1):
            self.tableWidget_2.close()
            table2status = table2status - 1
            self.tableWidget.show()
        else:
            self.tableWidget.show()
        table1status += 1

    def table2show(self):
        global Length_1, STX_O, CheckSum_O, Payload_O, table1status, table2status
        if (table1status == 1):
            self.tableWidget.close()
            table1status = table1status - 1
            self.tableWidget_2.show()
        else:
            self.tableWidget_2.show()
        table2status+=1



    def stop(self):
        global signal
        signal = "Stop"


    def pause(self):
        global signal
        # print("Paused")
        signal="Pause"

    def sleep(self,n):
        QtTest.QTest.qWait(n*1000)

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
        global STX, CheckSum, Length, Time, checksum, Payload_O, leng, n_rows, start, Number, msg, TS, TR, TP, Reserved, Payload
        query = self.textEdit.toPlainText()
        self.filename = fileName

        if msg==0: #Number로 콤보박스를 체크했을 경우
                for i in range(0,value1):
                    data = self.tableWidget.item(i,0)
                    txt=data.text()
                    # print(query+":"+txt)
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
                # print(query + ":" + txt)
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
                # print(query+":"+txt)

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
                # print(query+":"+txt)
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
                # print(query+":"+txt)

                if txt == query:  # 만약에 일치하는 경우

                    self.tableWidget_2.setItem(value2, 0, QTableWidgetItem(self.tableWidget.item(i, 0)))
                    self.tableWidget_2.setItem(value2, 1, QTableWidgetItem(self.tableWidget.item(i, 1)))
                    self.tableWidget_2.setItem(value2, 2, QTableWidgetItem(self.tableWidget.item(i, 2)))
                    self.tableWidget_2.setItem(value2, 3, QTableWidgetItem(self.tableWidget.item(i, 3)))
                    self.tableWidget_2.setItem(value2, 4, QTableWidgetItem(self.tableWidget.item(i, 4)))
                    self.tableWidget_2.setItem(value2, 5, QTableWidgetItem(self.tableWidget.item(i, 5)))
                    self.tableWidget_2.setItem(value2, 6, QTableWidgetItem(self.tableWidget.item(i, 6)))
                    value2 = value2 + 1

    def writeCsv(self):
        path = QFileDialog.getSaveFileName(self, 'Save CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], 'w') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                for row in range(self.tableWidget_2.rowCount()):
                    row_data = []
                    for column in range(self.tableWidget_2.columnCount()):
                        item = self.tableWidget_2.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                    writer.writerow(row_data)

    uartcom = threading.Thread(target=uart, args=())
    uartcom.start()

    print("스레드가 실행되었습니다.")



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

