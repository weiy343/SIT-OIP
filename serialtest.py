import time
import serial
import sys

arduino = serial.Serial("/dev/ttyACM0", 9600, timeout=10)
arduino.flush()

# For port to open
time.sleep(1)

# Writing
while True:
    print("Writing data")
    arduino.write(b'2')
    line = arduino.readline().decode('utf-8').rstrip()
    print(line)
    line = arduino.readline().decode('utf-8').rstrip()
    print(line)

# while True:
  #   if arduino.in_waiting:
        # Reading
  #       data = arduino.readline()
  #       print("Reading data: {}".format(data))
