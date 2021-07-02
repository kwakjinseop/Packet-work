import serial

ser = serial.Serial("COM3", 115200, timeout=1)
while True:
    print("insert op: ",end=" ")
    op = input()
    ser.write(op.encode())
    print("R:", ser.readline())

    if op is 'q':
        ser.close()