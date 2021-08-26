
from time import sleep
import serial
import sys

arduino = serial.Serial("/dev/ttyACM0", 9600, timeout=None)
arduino.flush()

# For port to open
sleep(1)

# 0 - 0 degrees, open drain
# 1 - 90 degrees, close drain
# 2 - check temperature
# 3 - check infrared
# 4 - pump water
# 5 - washing, ultrasonic
# 6 - fan
# 7 - heating coil
# 8 - LED strip
# 9 - off fan
# 10 - off heating

# def arduino_comm(msg):
#   arduino.write(msg.encode('utf-8'))
#   reply = arduino.readline().decode('utf-8').strip()
#   return reply

# arduino_comm("3")

# Process
# 3 check infra
print("Checking infrared")
arduino.write(b'3')
line = arduino.readline().decode('utf-8').strip()
print(line)

line = arduino.readline().decode('utf-8').strip()
print(line)

print("before i")
# 0 is open
# 1 is close
if line is "0":
  print("Compartment is open")
  sys.exit()

line = arduino.readline().decode('utf-8').strip()
print(line)

print("Starting washing process")
# 1 close drain
print("Closing drain")
arduino.write(b'1')
sleep(1)
line = arduino.readline().decode('utf-8').strip()
print(line)

# 4 pump water
print("Pumping water")
arduino.write(b'4')
sleep(1)
line = arduino.readline().decode('utf-8').strip()
print(line)
line = arduino.readline().decode('utf-8').strip()
print(line)
line = arduino.readline().decode('utf-8').strip()
print(line)

# 5 wash LED
print("Washing")
arduino.write(b'5')
sleep(1)
line = arduino.readline().decode('utf-8').strip()
print(line)
line = arduino.readline().decode('utf-8').strip()
print(line)
line = arduino.readline().decode('utf-8').strip()
print(line)

# 0 open drain
print("Opening drain")
arduino.write(b'0')
sleep(1)
line = arduino.readline().decode('utf-8').strip()
print(line)

# 1 close drain
print("Closing drain")
arduino.write(b'1')
sleep(1)
line = arduino.readline().decode('utf-8').strip()
print(line)

# 4 pump water
print("Pumping water")
arduino.write(b'4')
sleep(1)
line = arduino.readline().decode('utf-8').strip()
print(line)
line = arduino.readline().decode('utf-8').strip()
print(line)
line = arduino.readline().decode('utf-8').strip()
print(line)

# Reheat + sterilize

# 6 start fan & heating coil
print("Turning fan up")
arduino.write(b'6')
sleep(1)
line = arduino.readline().decode('utf-8').strip()
print(line)
# wait

# 7 heat up
#while loop readline to heat level
print("Heating up")
arduino.write(b'7')
sleep(1)
line = arduino.readline().decode('utf-8').strip()
print(line)
line = arduino.readline().decode('utf-8').strip()
print(line)

line = arduino.readline().decode('utf-8').strip()
print(line)

# temperature feedback
while float(line) < 80:
  sleep(1)
  arduino.write(b'7')
  line = arduino.readline().decode('utf-8').strip()
  print(line)
  line = arduino.readline().decode('utf-8').strip()
  print(line)

# complete
sleep(5)
line = arduino.readline().decode('utf-8').strip()
print(line)

# 0 open drain
print("Opening drain")
arduino.write(b'0')
sleep(1)
line = arduino.readline().decode('utf-8').strip()
print(line)

# complete
# off fan and heating coil
arduino.write(b'9')
sleep(1)
line = arduino.readline().decode('utf-8').strip()
print(line)
arduino.write(b'2')
sleep(1)
line = arduino.readline().decode('utf-8').strip()
print(line)
sleep(1)
arduino.write(b'8')
sleep(1)
line = arduino.readline().decode('utf-8').strip()
print(line)

# check cam