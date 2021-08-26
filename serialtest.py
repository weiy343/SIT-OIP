import time
import serial
import sys

arduino = serial.Serial("/dev/ttyACM0", 9600, timeout=10)
arduino.flush()

# For port to open
time.sleep(1)

# 0 - 0 degrees, open drain
# 1 - 90 degrees, close drain
# 2 - check temperature
# 3 - check infrared
# 4 - pump water
# 5 - washing, ultrasonic
# 6 - fan
# 7 - heating coil

# Process
# 3 check infra
print("Checking infrared")
arduino.write(b'3')
line = arduino.readline().decode('utf-8').strip()

# 0 is open
# 1 is close
if line is 0:
  print("Compartment is close")
  sys.exit()

print("Starting washing process")
# 1 close drain
print("Closing drain")
arduino.write(b'1')
# wait
line = arduino.readline().decode('utf-8').strip()
print(line)

# 4 pump water
print("Pumping water")
arduino.write(b'4')
# wait
line = arduino.readline().decode('utf-8').strip()
print(line)

# 5 wash LED
print("Washing")
arduino.write(b'5')
# wait
line = arduino.readline().decode('utf-8').strip()
print(line)

# 0 open drain
print("Opening drain")
arduino.write(b'0')
# wait
line = arduino.readline().decode('utf-8').strip()
print(line)

# 1 close drain
print("Closing drain")
arduino.write(b'1')
# wait
line = arduino.readline().decode('utf-8').strip()
print(line)

# 4 pump water
print("Pumping water")
arduino.write(b'4')
# wait
line = arduino.readline().decode('utf-8').strip()
print(line)

# Reheat + sterilize

# 6 start fan & heating coil
print("Turning fan up")
arduino.write(b'6')
line = arduino.readline().decode('utf-8').strip()
# wait

# 7 heat up
#while loop readline to heat level
print("Heating up")
arduino.write(b'7')
line = arduino.readline().decode('utf-8').strip()
print(line)

# temperature feedback
while float(line) < 40:
  line = arduino.readline().decode('utf-8').strip()
  print(line)

# complete
line = arduino.readline().decode('utf-8').strip()
print(line)

# 0 open drain
print("Opening drain")
arduino.write(b'0')
# wait
line = arduino.readline().decode('utf-8').strip()
print(line)

# complete
line = arduino.readline().decode('utf-8').strip()
print(line)

# check cam