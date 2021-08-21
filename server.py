from flask import Flask, request, jsonify, render_template, send_file
# from picamera import PiCamera
from time import sleep

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pump")
def pumping_process():
    print("pumping.")
    return jsonify({
        "status": "Pumping water",
        "time": 3,
    })

@app.route("/wash")
def washing_process():
    print("washing.")
    return jsonify({
        "status": "Washing",
        "time": 3,
    })

@app.route("/drain")
def draining_process():
    print("draining.")
    return jsonify({
        "status": "Draining",
        "time": 3,
    })

@app.route("/dry")
def drying_process():
    print("drying.")
    return jsonify({
        "status": "Drying",
        "time": 3,
    })

@app.route("/sterilize")
def sterilizing_process():
    print("sterilizing.")
    return jsonify({
        "status": "Sterilizing",
        "time": 3,
    })

# def take_picture():
#     camera = PiCamera()
#     camera.start_preview()
#     sleep(5)
#     camera.capture('./images/image.jpg')
#     camera.stop_preview()
#     pass

@app.route("/start")
def start():
    return jsonify({
        "status": "Pumping water",
        "time": 10,
    })
    # take_picture()

if __name__ == "__main__":
    app.run(debug=True)