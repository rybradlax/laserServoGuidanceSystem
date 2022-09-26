import serial
import time
import struct



class transmitData:

   def send(theta):
    ser = serial.Serial('COM4', 115200, timeout = 0.5)
    #addr = 0x255 # bus address, can send signals 0-255, for speed
   # addr2 = 0x10 # can send signals 0-10, for time
   # bus = SMBus(1) # indicates /dev/ic2-1
   # #bus.write_byte(addr, 0x10) # actually sends data to arduino
    ser.write(theta)
    time.sleep(0.5)  
    line = ser.read(3)
    strLine = line.decode()
    strLine = strLine.strip()
    if len(strLine) == 0:
        intLine = -50
    else:
        intLine = int(strLine)
    ser.flush()
    return intLine
   
   def send2(s):
    ser = serial.Serial('COM4', 115200, timeout = 0.2)
    #addr = 0x255 # bus address, can send signals 0-255, for speed
   # addr2 = 0x10 # can send signals 0-10, for time
   # bus = SMBus(1) # indicates /dev/ic2-1
   # #bus.write_byte(addr, 0x10) # actually sends data to arduino
    #print(s.encode())
    ser.write(s.encode())
    time.sleep(0.1)

