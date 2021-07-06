import PyQt5.QtWidgets as qtwid
import serial
import sys
import numpy as np
import time
from PyQt5 import QtWidgets, QtCore


value1 = 0
class MainWindow(qtwid.QMainWindow):


    def __init__(self):
        super().__init__()
        self.te_query = qtwid.QTextEdit(self) #문자열 입력부분
        self.btn_confirm = qtwid.QPushButton("확인",self)
        # self.lb_query = qtwid.QLabel("[입력 문자열]",self)
        self.tableWidget = qtwid.QTableWidget(self)
        self.Initialize()

    def Initialize(self):
        self.setWindowTitle("Button 클릭하면 TextEdit에 입력 내용을 Label에 표시")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(20)
        self.setGeometry(300, 100, 600, 400)
        self.tableWidget.resize(1000, 500)
        self.tableWidget.horizontalHeader().setSectionResizeMode(qtwid.QHeaderView.Stretch)
        self.setTableWidgetData()

        self.te_query.move(10,510) #문자열 입력부분
        self.te_query.resize(300,40) #문자열 입력부분
        self.btn_confirm.move(330,510) #확인 버튼
        self.btn_confirm.resize(100,40) #확인버튼
        # self.lb_query.move(20,100)
        # self.lb_query.resize(600,40)
        self.btn_confirm.clicked.connect(self.uart)

    def setTableWidgetData(self):
        column_headers = ['STX', 'Time', 'Checksum', 'Respond', 'Length', 'Payload']
        result_array = np.array([0xab, 0x1c, 0x3b, 0xf3, 0x75, 0x46, 0x14, 0x28, 0xf2, 0xca, 0xb4, 0xe7, 0xd6, 0x08, 0x00, 0x44, 0x89, 0xaa, 0xac, 0xff, 0xfa])


        # print(result_array[0:2])
        self.tableWidget.setHorizontalHeaderLabels(column_headers)

        self.tableWidget.setItem(value1, 0, qtwid.QTableWidgetItem(str(hex(result_array[0]))))  # STX
        self.tableWidget.setItem(value1, 1, qtwid.QTableWidgetItem(str(hex(sum(result_array[1:5])))))  # Time
        self.tableWidget.setItem(value1, 2, qtwid.QTableWidgetItem(str(hex(sum(result_array[5:9])))))  # Checksum
        self.tableWidget.setItem(value1, 3, qtwid.QTableWidgetItem(str(hex(sum(result_array[9:13]))))) # Respond
        self.tableWidget.setItem(value1, 4, qtwid.QTableWidgetItem(str(hex(sum(result_array[13:15])))))  # Length
        self.tableWidget.setItem(value1, 5, qtwid.QTableWidgetItem(str(hex(sum(result_array[15:21])))))  # Payload

    # def Btn_confirmClick(self):
    #     query = self.te_query.toPlainText()
    #     self.te_query.setText("")
    #     self.lb_query.setText(query)

    def uart(self):
        global value1
        query = self.te_query.toPlainText()
        ser = serial.Serial("COM3", 115200, timeout=1)
        # op = query
        op = b'ab 3b:f3:75:46:14:d8:f2:ca:b4:e7:d6:08:00'
        x = str(op)
        print(x)
        a = str(op.split(":")[0])
        # b = str(op.split(":")[1])
        # c = str(op.split(":")[2])
        # d = str(op.split(":")[3])
        # e = str(op.split(":")[4])
        # f = str(op.split(":")[5])
        #
        print(a)
        # print(b)
        # print(c)
        # print(d)
        # print(e)
        # print(f)

        ser.write(op.encode()) #값 입력
        print("R:", ser.readline())
        str_data = str(ser.readline(), 'utf-8')
        # print(str_data)
        hex_int = int(str_data, 16)
        length = len(str_data)

        # self.tableWidget.setItem(value1, 1, qtwid.QTableWidgetItem(a)) #STX
        # self.tableWidget.setItem(value1, 2, qtwid.QTableWidgetItem(str(op.split(':')[1]))) #Time
        # self.tableWidget.setItem(value1, 3, qtwid.QTableWidgetItem(str(op.split(':')[2]))) #Checksum
        # self.tableWidget.setItem(value1, 4, qtwid.QTableWidgetItem(str(op.split(':')[3]))) #Respond
        # self.tableWidget.setItem(value1, 5, qtwid.QTableWidgetItem(str(op.split(':')[4]))) #Length
        # self.tableWidget.setItem(value1, 6, qtwid.QTableWidgetItem(time.strftime(str(op.split(':')[2])))) #Payload

        value1=value1+1
        if op is 'q':
            ser.close()
        print(value1)
        print(len(str_data))

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




