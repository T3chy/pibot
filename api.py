import time
import flask
from flask import request
import Adafruit_PCA9685
pwm = Adafruit_PCA9685.PCA9685()
# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
pwm.set_pwm_freq(60)
def turn(degrees):
    degrees = float(degrees)
    if abs(degrees) == degrees:
        dir = "right"
    else:
        dir = "left"
        degrees = abs(degrees)
    if degrees > 90:
        print("input over 90 degrees, returning 90 degrees")
        degrees = 90
    center = (servo_max - servo_min) / 2 + servo_min
    rightang = (servo_max - servo_min) / 2
    if degrees == 0:
        return int(center)
    if dir == "right":
        return int((degrees / 90) * rightang + center)
    else:
        return int((degrees / 90) * rightang - center)

def forward(turndeg=0):
        pwm.set_pwm(2,0,turn(turndeg))
        pwm.set_pwm(0,0,servo_min)
        pwm.set_pwm(1,0,servo_max)
def backward(turndeg=0):
        pwm.set_pwm(2,0,turn(turndeg))
        pwm.set_pwm(0,0,servo_max)
        pwm.set_pwm(1,0,servo_min)
def stop():
        pwm.set_all_pwm(0,1)

app = flask.Flask(__name__)

@app.route('/move', methods=['GET','PUT'])
def move():
    if request.method == "PUT":
        dir = request.form["dir"]
        if dir == "forward":
            forward(turndeg=request.form["turndeg"])
            return("going forward")
        elif dir == "backward":
            backward(turndeg=request.form["turndeg"])
            return("going backward")
        else:
            stop()
            return("stopping")
    else:
        return("still alive")
    
app.run(host='0.0.0.0')