import serial


def uart(self):  # 20개의 패킷이 들어옴 //15부터 payload
    query = self.te_query.toPlainText()
    ser = serial.Serial("COM3", 115200, timeout=1)
    op = query
    a = op.split(" ")
    x = bytearray(a)


    if (a == "q"):
        ser.close()

    # print(type(a[15]