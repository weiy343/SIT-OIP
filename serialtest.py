from flask import Flask, request, jsonify, render_template, send_file
from picamera import PiCamera
from time import sleep
from flask_socketio import SocketIO, send, emit
import serial
import sys

# WebSocket
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
socketio = SocketIO(app)

# Serial communication
arduino = serial.Serial("/dev/ttyACM0", 9600, timeout=None)
arduino.flush()

# For port to open
sleep(1)

# Serial functions
def sendToArduino(command, timer):
  arduino.write(command.encode('utf-8'))
  arduino.write(timer.encode('utf-8'))

# Entire washing process including pumping, washing and draining
def wash(timer):
  sendToArduino(0, timer)
  isOpen = arduino.readline().decode('utf-8').strip()
  if isOpen is "0":
    emit("coverWarning", "Please close the cover.")
    return
  
  # Pump
  emit("message", {
      "status": "Pumping water in progress...",
      "time": timer
  })
  pump = arduino.readline().decode('utf-8').strip()
  
  # Wash
  emit("message", {
      "status": "Washing in progress...",
      "time": timer
  })
  wash = arduino.readline().decode('utf-8').strip()
  
  # Drain
  emit("message", {
      "status": "Draining water in progress...",
      "time": timer
  })
  drain = arduino.readline().decode('utf-8').strip()
  return

# Entire sterilizing process including pumping, heating, sterilizing and draining
def sterilize(timer):
  sendToArduino(1, timer)
  # Pump
  emit("message", {
      "status": "Pumping water in progress...",
      "time": timer
  })
  pump = arduino.readline().decode('utf-8').strip()

  # Sterilize
  checkTemp()
  emit("message", {
      "status": "Sterilizing in progress...",
      "time": timer
  })
  sterilize = arduino.readline().decode('utf-8').strip()

  # Drain
  emit("message", {
      "status": "Sterilizing in progress...",
      "time": timer
  })
  drain = arduino.readline().decode('utf-8').strip()

# Entire drying process including heating and drying
def dry(timer, retry):
  sendToArduino(2, timer)

  status = "Drying in progress..."

  if retry > 0:
      status = f"Drying ({retry}) in progress..."
  
  # Dry
  checkTemp()
  emit("message", {
      "status": status,
      "time": timer
  })
  dry = arduino.readline().decode('utf-8').strip()

# Camera
def checkDry(timer):
  emit("check", "Checking dryness...")
  sendToArduino(3, timer)
  with PiCamera() as camera:

      camera.start_preview()
      sleep(timer)
      camera.capture('./images/image.jpg')
      camera.stop_preview()
      
  # Processing here

  # Depends on camera
  return False

# Heating temperature check
def checkTemp():
  temp = arduino.readline().decode('utf-8').strip()
  while float(temp) < 70:
    temp = arduino.readline().decode('utf-8').strip()
    emit("heating", {
      "status": "Heating in progress...",
      "temp": temp
    })

# Web APIs
@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("message")
def startProcess():

    iterations = 0

    wash(10)
    sterilize(10)
    dry(10, iterations)

    isDry = checkDry(5)
    while(not isDry):
        iterations =+ 1
        dry(10, iterations)
        isDry = checkDry(5)

        # Simulation 1 loop
        break
    emit("complete")