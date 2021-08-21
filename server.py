from flask import Flask, request, jsonify, render_template, send_file

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start")
def start():
    print("hello.")

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

if __name__ == "__main__":
    app.run(threaded=True, port=5000)