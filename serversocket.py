from flask import Flask, request, jsonify, render_template, send_file
from picamera import PiCamera
from time import sleep
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
socketio = SocketIO(app)
# camera = PiCamera()

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("message")
def startProcess(msg):
    print(msg)
    iterations = 0
    pumping_process(5)
    washing_process(5)
    draining_process(5)
    drying_process(5, iterations)
    sterilizing_process(5, iterations)
    isClean = take_picture(5)
    while(not isClean):
        iterations =+ 1
        drying_process(5, iterations)
        sterilizing_process(5, iterations)
        isClean = take_picture(5)
        break
    emit("complete")

def pumping_process(time):
    emit("message", {
        "status": "Pumping water in progress...",
        "time": time
    })
    socketio.sleep(time)

def washing_process(time):
    emit("message", {
        "status": "Washing in progress...",
        "time": time
    })
    socketio.sleep(time)

def draining_process(time):
    emit("message", {
        "status": "Draining in progress...",
        "time": time
    })
    socketio.sleep(time)

def drying_process(time, retry):

    status = "Drying in progress..."

    if retry > 0:
        status = f"Drying ({retry}) in progress..."

    emit("message", {
        "status": status,
        "time": time,
    })
    socketio.sleep(time)

def sterilizing_process(time, retry):

    status = "Sterilizing in progress..."

    if retry > 0:
        status = f"Sterilizing ({retry}) in progress..."

    emit("message", {
        "status": status,
        "time": time
    })
    socketio.sleep(time)

def take_picture(time):
    emit("check", "Checking cleanliness...")

    with PiCamera() as camera:

        camera.start_preview()
        sleep(5)
        camera.capture('./images/image.jpg')
        camera.stop_preview()

    socketio.sleep(time)

    # Depends on camera
    return False

if __name__ == "__main__":
    socketio.run(app, debug=True)