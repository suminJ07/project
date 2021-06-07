import RPi.GPIO as GPIO
from flask import Flask, render_template, url_for, redirect, Response, request
from gpiozero import LEDBoard
from camera import Camera
import adafruit_dht
from board import *

app = Flask(__name__)

GPIO.setwarnings(False)  
GPIO.setmode(GPIO.BCM) 
GPIO.setup(20, GPIO.OUT, initial=GPIO.LOW)

SENSOR_PIN = D17
dht11 = adafruit_dht.DHT11(SENSOR_PIN, use_pulseio=False)

@app.route("/")
def home():
    DHT = { 'temp' : dht11.temperature , 'humi' : dht11.humidity}
    return render_template("index.html", **DHT)

@app.errorhandler(500)
def page_not_found(error):
     return render_template('pagenf.html'), 500

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/led/on")
def led_on():
        GPIO.output(20, GPIO.HIGH)
        return "ok"


@app.route("/led/off")
def led_off():
        GPIO.output(20, GPIO.LOW)
        return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001, threaded=True, debug=False)

