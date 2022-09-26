import serial
import time
import struct




ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
#addr = 0x255 # bus address, can send signals 0-255, for speed
# addr2 = 0x10 # can send signals 0-10, for time
# bus = SMBus(1) # indicates /dev/ic2-1
# #bus.write_byte(addr, 0x10) # actually sends data to arduino
x = 32
ser.write(str(x))
time.sleep(1)
ser.flush()
