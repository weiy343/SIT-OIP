from flask import Flask, request, jsonify, render_template, send_file
# from picamera import PiCamera
from time import sleep

def pumping_process():
    print("pumping.")
    pass

def washing_process():
    print("washing.")
    pass

def draining_process():
    print("draining.")
    pass

def drying_process():
    print("draining.")
    pass

def sterilizing_process():
    print("sterilizing.")
    pass

# def take_picture():
#     camera = PiCamera()
#     camera.start_preview()
#     sleep(5)
#     camera.capture('./images/image.jpg')
#     camera.stop_preview()
#     pass

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start")
def start():
    print("hello.")
    # take_picture()

if __name__ == "__main__":
    app.run(debug=True)