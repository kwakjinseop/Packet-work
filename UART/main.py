import sys
import serial
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType(r'C:\Users\Geoplan\Desktop\곽진섭_인턴\design.ui')[0]


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.uart)

    # def click_button(self):
    #     exist_lineEdit = self.lineEdit.text()
    #     self.lineEdit.setText(exist_lineEdit + self.pushButton.text())
    #     self.tableWidget.setColumnCount(1)
    #     self.tableWidget.setRowCount(20)
    #     for i in range(20):
    #         for value in range(1):
    #             self.tableWidget.setItem(i, value, QTableWidgetItem(self.uart()))
    def uart(self):
        ser = serial.Serial("COM3", 115200, timeout=1)
        # while True:
        print("insert op: ", end=" ")
        op = input()
        ser.write(op.encode())
        print("R:", ser.readline())

        exist_lineEdit = self.lineEdit.text()
        self.lineEdit.setText(exist_lineEdit + self.pushButton.text())
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(20)
        for i in range(20):
            for value in range(1):
                self.tableWidget.setItem(i, value, QTableWidgetItem(ser.readline()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
