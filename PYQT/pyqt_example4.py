import sys
import serial
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSerialPort import *



class MyApp(QWidget):


    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.btn = QPushButton('Button', self)
        self.btn.move(30,30)
        self.btn.clicked.connect(self.showDialog)

        self.le = QLineEdit(self)
        self.le.move(120,35)
        self.setGeometry(300,300,300,200)
        self.show()



    def showDialog(self):

        ser = serial.Serial("COM3", 115200, timeout=1)
        while True:
            op, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter data:')
            ser.write(op.encode())
            print("R:", ser.readline())
            if ok:
                self.le.setText(ser.readline())
            if op is 'ssss':
                ser.close()



    # def emit(self, record):
    #     self.target_widget.append(record.asctime + ' -- ' + record.getMessage())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())

