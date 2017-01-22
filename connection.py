import time
import serial
import urllib.request

# Open connection
ser = serial.Serial('/dev/ttyACM0', 9600)
#ser = serial.Serial('COM4', 9600)

while True:
    
    # Read from serial, send to website
    line = ser.readline().decode('UTF-8')
    if len(line) > 4 and line[:4] == 'temp':
        print(line)
        sendURL = 'HTTP://192.168.1.18/send.php?' + line 
        print(urllib.request.urlopen(sendURL).read())
    else:
        while len(line) > 2:
            print(line)
            line = ser.readline().decode('UTF-8')

    # Read from website, send to serial
    recieveURL = 'HTTP://192.168.1.18/recieve.php'
    response = urllib.request.urlopen(recieveURL).read()
    ser.write(response)
    print(response)
    
    time.sleep(9)

ser.close()