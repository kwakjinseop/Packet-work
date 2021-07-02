import time
from time import sleep
import serial
ser = serial.Serial("COM3", baudrate = 9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
while 1:
    rx_data =ser.readline()
    print(rx_data)
    ser.write(rx_data)