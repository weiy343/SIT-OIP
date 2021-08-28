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
  arduino.write(repr(command).encode('utf-8'))
  arduino.write(repr(timer).encode('utf-8'))

# Entire washing process including pumping, washing and draining
def wash(timer):
  emit("message", {
      "status": "Pumping water in progress...",
      "time": timer
  })

  socketio.sleep(1)
  pump = arduino.readline().decode('utf-8').strip()
  print("pumping: ", pump)

  # Wash
  emit("message", {
      "status": "Washing in progress...",
      "time": timer
  })

  socketio.sleep(1)
  wash = arduino.readline().decode('utf-8').strip()
  print("washing: ", wash)
  
  # Drain
  emit("message", {
      "status": "Draining water in progress...",
      "time": timer
  })

  socketio.sleep(1)
  drain = arduino.readline().decode('utf-8').strip()
  print("draining: ", drain)  
  return

# Entire sterilizing process including pumping, heating, sterilizing and draining
def sterilize(timer):
  sendToArduino(1, timer)
  # Pump
  emit("message", {
      "status": "Pumping water in progress...",
      "time": timer
  })

  socketio.sleep(1)
  pump = arduino.readline().decode('utf-8').strip()
  print("pumping: ", pump)

  # Sterilize
  checkTemp()
  emit("message", {
      "status": "Sterilizing in progress...",
      "time": timer
  })

  socketio.sleep(1)
  sterilize = arduino.readline().decode('utf-8').strip()
  print("Sterilizing: ", sterilize)

  # Drain
  emit("message", {
      "status": "Draining in progress...",
      "time": timer
  })

  socketio.sleep(1)
  drain = arduino.readline().decode('utf-8').strip()
  print("draining: ", drain)

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
  socketio.sleep(1)
  dry = arduino.readline().decode('utf-8').strip()
  print("Drying: ", dry)

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
  print("temp: ", temp)
  while float(temp) < 78:
    emit("heating", {
      "status": "Heating in progress...",
      "temp": temp
    })
    socketio.sleep(1)
    temp = arduino.readline().decode('utf-8').strip()

# Web APIs
@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("message")
def startProcess():

    iterations = 0

    sendToArduino(0, 10)
    isOpen = arduino.readline().decode('utf-8').strip()
    print("THIS IS OPEN: ", isOpen)
    if isOpen is "1":
      print("open")
      emit("coverWarning", "Please close the cover.")
      return

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

if __name__ == "__main__":
    socketio.run(app, debug=True)