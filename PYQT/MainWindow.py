import PyQt5.QtWidgets as qtwid
import serial
import sys
import time
import protocol


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
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(20)
        self.setGeometry(300, 100, 600, 400)
        self.tableWidget.resize(500, 500)
        self.setTableWidgetData()

        self.te_query.move(10,510) #문자열 입력부분
        self.te_query.resize(300,40) #문자열 입력부분
        self.btn_confirm.move(330,510) #확인 버튼
        self.btn_confirm.resize(100,40) #확인버튼
        # self.lb_query.move(20,100)
        # self.lb_query.resize(600,40)
        self.btn_confirm.clicked.connect(self.uart)

    def setTableWidgetData(self):
        column_headers = ['Time', 'Checksum', 'Respond', 'Length', 'Payload']
        result_array = [0xAB, ]
        self.tableWidget.setHorizontalHeaderLabels(column_headers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(qtwid.QHeaderView.Stretch)

    # def Btn_confirmClick(self):
    #     query = self.te_query.toPlainText()
    #     self.te_query.setText("")
    #     self.lb_query.setText(query)

    def uart(self):
        global value1
        query = self.te_query.toPlainText()
        ser = serial.Serial("COM3", 115200, timeout=1)
        op = query
        ser.write(op.encode()) #값 입력
        # print("R:", ser.readline())
        str_data = str(ser.readline(), 'utf-8')
        print(str_data)
        length = len(str_data)

        self.tableWidget.setItem(value1, 1, qtwid.QTableWidgetItem(str_data))  # 표부분
        self.tableWidget.setItem(value1, 0, qtwid.QTableWidgetItem(time.strftime('%H:%M:%S')))
        self.tableWidget.setItem(value1, 3, qtwid.QTableWidgetItem(str(length)))
        value1=value1+1
        if op is 'q':
            ser.close()
        print(value1)
        print(len(str_data))





if __name__ == "__main__":
    app = qtwid.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    app.exec()




