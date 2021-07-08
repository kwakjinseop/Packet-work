from PyQt5.QtWidgets import *
import serial, random, string, sys, secrets
from PyQt5.QtCore import *
import threading, time





value1 = 1
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

class MainWindow(QMainWindow):
    def __init__(self): #칼럼: 6, 로우: 20
        global STX_O, CheckSum_O, Length_0, checksum, Payload_O
        super().__init__()

        self.query = QLineEdit()
        self.query.setPlaceholderText("Search...")
        self.query.textChanged.connect(self.search)

        n_rows = 20
        n_cols = 6
        self.table = QTableWidget()
        self.table.setRowCount(n_rows)
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
        self.btn_button.clicked.connect(self.uart)


        column_headers = ['STX', 'Time', 'Checksum', 'Reserved', 'Length', 'Payload']
        self.table.setHorizontalHeaderLabels(column_headers)

        self.table.setItem(0, 0, QTableWidgetItem((hex(packet[0]))))  # STX
        STX_O = str(hex(packet[0]))
        self.table.setItem(0, 1, QTableWidgetItem(str.join("", ("0x%02X " % i for i in packet[1:5]))))  # Time
        self.table.setItem(0, 2, QTableWidgetItem(str.join("", ("0x%02X " % i for i in packet[6:9]))))  # Checksum
        CheckSum_O = str.join("", ("0x%02X " % i for i in packet[6:9]))
        self.table.setItem(0, 3, QTableWidgetItem(str.join("", ("0x%02X " % i for i in packet[10:14]))))  # Reserved
        self.table.setItem(0, 5,QTableWidgetItem(str.join("", ("0x%02X " % i for i in packet[15:]))))  # Payload
        Payload_O = sum(packet[15:])


        Length_0 = str.join("", ("0x%02X " % i for i in packet[15:]))

        self.table.setItem(0, 5, QTableWidgetItem(str.join("", ("0x%02X " % i for i in packet[14:]))))  # Payload



    def search(self, s): # 검색기능 함수
        items = self.table.findItems(s, Qt.MatchContains)
        if items:
            item = items[0]
            self.table.setCurrentItem(item)


    def uart(self):  # 20개의 패킷이 들어옴 //15부터 payload
        global value1
        global packet
        global STX, CheckSum, Length, Time, checksum, Payload_O, leng
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
        print(CheckSum)

        print(Payload_O)

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
            print(Length)
            Reserved = " ".join(a[10:14])
            Payload = " ".join(a[15:])
        else:
            STX = "False"
            Time = "False"
            checksum = "False"
            Reserved = "False"
            Payload = "False"
            Length = "False"

        self.table.setItem(value1, 0, QTableWidgetItem(STX))  # STX
        self.table.setItem(value1, 1, QTableWidgetItem(Time))  # Time
        self.table.setItem(value1, 2, QTableWidgetItem(checksum))  # Checksum
        self.table.setItem(value1, 3, QTableWidgetItem(Reserved))  # Respond
        self.table.setItem(value1, 4, QTableWidgetItem(str(Length)))  # Length
        self.table.setItem(value1, 5, QTableWidgetItem(Payload))  # Payload

        value1 = value1 + 1
        CheckSum = 0




    def DebugChecking(str):
        cnt = 0
        while(cnt<10):
            time.sleep(random.randint(0, 100) / 300.0)
            print(str, cnt)
            cnt += 1
            print("=== ", str, "스레드 종료 ===")


    cnt = threading.Thread(target = uart , args=(1,))
    cnt2 = threading.Thread(target= DebugChecking, args=("체크용",))
    print("===Thread Operating===")
    cnt.start()
    cnt2.start()

    cnt2.join()
    print("체크종료")


if __name__ == "__main__":
    app = QApplication([])
    mw = MainWindow()
    mw.show()

    app.exec()