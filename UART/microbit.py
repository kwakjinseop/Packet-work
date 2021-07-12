import serial
import threading
import time
import random


def DoitThread():
    ser = serial.Serial("COM3", 115200, timeout=1)
    while True:
        print("insert op: ",end=" ")
        op = input()
        a = op.split(" ") #띄어쓰기에 따라 문자열 분리
        ser.write(op.encode())
        print("R:", ser.readline())
        print(op)
        if(op=="q"):
            ser.close()
            th_a.join()
            print("=== 스레드 종료 ===")


th_a = threading.Thread(target=DoitThread)

print("==스레드 가동==")
th_a.start()



