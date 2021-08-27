
from time import sleep
import serial
import sys

arduino = serial.Serial("/dev/ttyACM0", 9600, timeout=None)
arduino.flush()

# For port to open
sleep(1)

# 0 - open drain
# 1 - close drain
# 2 - cover
# 3 - pump
# 4 - wash
# 5 - on fan
# 6 - off fan
# 7 - on heat
# 8 - off heat
# 9 - led

# def arduino_comm(msg):
#   arduino.write(msg.encode('utf-8'))
#   reply = arduino.readline().decode('utf-8').strip()
#   return reply

# arduino_comm("3")

def countdown(seconds):
  for x in range(seconds, 0, -1):
    print(x)
    sleep(1)

# Process
# 3 check infra
print("Checking infrared")
arduino.write(b'2')

line = arduino.readline().decode('utf-8').strip()

# 0 is open
# 1 is close
if line is "0":
  print("Compartment is open")
  sys.exit()

print("Starting washing process")

# 1 close drain
print("Closing drain")
arduino.write(b'1')

# 3 pump water
print("Pumping water")
arduino.write(b'3')

# wait to finish
line = arduino.readline().decode('utf-8').strip()
print(line)

# 4 wash LED
print("Washing")
arduino.write(b'4')

# wait to finish
line = arduino.readline().decode('utf-8').strip()
print(line)

# 0 open drain
print("Opening drain")
arduino.write(b'0')

# 1 close drain
print("Closing drain")
arduino.write(b'1')

# Sterilizing process
# 3 pump water
print("Pumping water")
arduino.write(b'3')
# wait to finish
line = arduino.readline().decode('utf-8').strip()
print(line)

# 5 start fan
print("Turning fan up")
arduino.write(b'5')

# 7 heat up
#while loop readline to heat level
print("Heating up")
arduino.write(b'7')

line = arduino.readline().decode('utf-8').strip()
print(line)

# temperature feedback
while float(line) < 80:

  arduino.write(b'7')
  line = arduino.readline().decode('utf-8').strip()
  print(line)

# Complete
print("Heated. Sterilizing...")

countdown(10)

# 0 open drain
print("Opening drain")
arduino.write(b'0')

# complete
# off fan and heating coil
print("Off fan")
arduino.write(b'6')

print("Off Heat")
arduino.write(b'8')

print("Led check")
arduino.write(b'9')
# check cam