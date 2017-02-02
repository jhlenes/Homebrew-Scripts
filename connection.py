import time
import serial
import urllib.request
import sys
import glob

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

while True:
    try:
        # Open connection
        ports = serial_ports()
        if len(ports) == 0:
            raise EnvironmentError('Arduino is not connected')
        print('connecting to arduino on: ' + ports[0])
        ser = serial.Serial(ports[0], 9600, timeout=5)
        
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
            
            time.sleep(30)
        
        ser.close()
    except BaseException as e:
        print('Error: ' + str(e))
        print('Trying again...')
        time.sleep(30)
        
        