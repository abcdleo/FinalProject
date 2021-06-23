import serial

# XBee setting
serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev, 9600)

# send to remote
# s.write("abcd\r\n".encode())
while(True):
    line = s.read(32)
    print('Get:', line.decode())

s.close()