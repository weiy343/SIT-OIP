from flask import Flask, request, jsonify, render_template, send_file
# from picamera import PiCamera
from time import sleep
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("message")
def startProcess(msg):
    print(msg)
    pumping_process(5)
    washing_process(5)
    draining_process(5)
    drying_process(5)
    sterilizing_process(5)
    isClean = take_picture(5)
    while(not isClean):
        drying_process(5)
        sterilizing_process(5)
        isClean = take_picture(5)
        break
    emit("complete")

def pumping_process(time):
    emit("message", {
        "status": "Pumping",
        "time": time
    })
    socketio.sleep(time)

def washing_process(time):
    emit("message", {
        "status": "Washing",
        "time": time
    })
    socketio.sleep(time)

def draining_process(time):
    emit("message", {
        "status": "Draining",
        "time": time
    })
    socketio.sleep(time)

def drying_process(time):
    emit("message", {
        "status": "Drying",
        "time": time
    })
    socketio.sleep(time)

def sterilizing_process(time):
    emit("message", {
        "status": "Sterilizing",
        "time": time
    })
    socketio.sleep(time)

def take_picture(time):
    emit("check", "Checking cleanliness...")

    # camera = PiCamera()
    # camera.start_preview()
    # sleep(5)
    # camera.capture('./images/image.jpg')
    # camera.stop_preview()

    socketio.sleep(time)

    # Depends on camera
    return False

if __name__ == "__main__":
    socketio.run(app, debug=True)