#!/usr/bin/env python
import glob
import json
import sys
import time

import requests
import serial

# delays in seconds
UPDATE_DELAY = 60
SEND_DELAY = 5 * 60
RETRY_CONNECTION_DELAY = 30

BASE_URL = "HTTP://localhost"

NOT_RUNNING = -1

batch_id = NOT_RUNNING
start_time = 0.0  # time in seconds
send_time = 0.0


def serial_ports():
    """ Lists serial port names.

        :raises EnvironmentError:
            On unsupported or unknown platforms.
        :returns:
            A list of the serial ports available on the system.
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError("Unsupported platform")

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def get_serial():
    """ Gets the first available serial port.

    :raises EnvironmentError:
        On no available ports.
    :returns:
        Serial.
    """
    ports = serial_ports()
    if len(ports) == 0:
        raise EnvironmentError("Arduino is not connected.")
    print("Connecting to Arduino on: " + ports[0])
    return serial.Serial(ports[0], 9600, timeout=5)


def update_temperature_data(ser):
    """ Gets latest temperature data from serial and sends it to the website.

    :param ser:
        The serial connection.
    """
    global send_time
    global batch_id
    line = ser.readline().decode('UTF-8')
    if len(line) > 4 and line[:4] == 'temp':
        if time.time() - send_time > SEND_DELAY:
            send_time = time.time()
            send_url = BASE_URL + "/send/?id=" + batch_id + "&" + line
            print("Data sent to website:", line)
            print("Response from website:", requests.get(send_url).text)
        else:
            # the data will not be inserted into the database, but instead used to show realtime stats on the page
            send_url = BASE_URL + "/send/?id=" + batch_id + "&" + line + "&update"
            print("Data sent to website:", line)
            print("Response from website:", requests.get(send_url).text)

    else:  # system not active or some small error
        while len(line) > 2:  # empty the buffer
            print("Emptying the buffer:", line)
            line = ser.readline().decode('UTF-8')


def get_setpoint():
    """ Gets the batch_id and setpoint from the website as json
    :return:
        setpoint
    """
    global batch_id
    receive_url = BASE_URL + "/receive"
    response = requests.get(receive_url).text

    data = json.loads(response)
    if 'batch_id' in data:
        batch_id = data['batch_id']
        if batch_id > 0:
            setpoint = data['setpoint']
            return setpoint
    return NOT_RUNNING


def main():
    while True:
        try:
            # get serial connection
            ser = get_serial()
            while True:
                # update website with latest temperature data from serial
                update_temperature_data(ser)

                # get setpoint from website and send it to the serial
                setpoint = get_setpoint()
                ser.write(';;{:.1f}'.format(setpoint))
                print("Setpoint sent to Arduino: {:.1f}".format(setpoint))

                # wait
                print("\n")
                time.sleep(UPDATE_DELAY)

        except BaseException as e:
            print("Error:", str(e))
            print("Trying again...\n")
            time.sleep(RETRY_CONNECTION_DELAY)


if __name__ == "__main__":
    main()
