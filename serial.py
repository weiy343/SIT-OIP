from time import time
import serial
import sys

arduino = serial.Serial("/dev/ttyUSB0", 9600, timeout=10)

input = sys.argv[1]

# Writing
print("Writing data: {}".format(input))
arduino.write(str.encode(input))

# Reading
data = arduino.readline()
print("Reading data: {}".format(data))
