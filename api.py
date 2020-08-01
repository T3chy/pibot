import time
import flask
from flask import request
import Adafruit_PCA9685
import time
import board
import neopixel
pixel_pin = board.D18
num_pixels = 8
ORDER = neopixel.GRB
 
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)
pwm = Adafruit_PCA9685.PCA9685()
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
pwm.set_pwm_freq(60)
signal = ""
pixels.fill((0,0,0))
pixels.show()
def turn(degrees,isstop=False):
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
    print("turning " + str(degrees) + " degrees to the " + dir)
    if not isstop:
        if signal != dir:
            lightsoff()
            turnsignal(dir)
    else:
        lightsoff()
        turnsignal("stop")
    if degrees == 0:
        return int(center)
    if dir == "right":
        return int((degrees / 90) * rightang + center)
    else:
        print(int((degrees / 90) * rightang))
        return int(center - ((degrees / 90) * rightang))
def lightsoff():
    for i in num_pixels:
        pixels.fill((0,0,0))
    pixels.show()
def turnsignal(dir):
    if dir == "left":
        dir = [0]
    elif dir == "right":
        dir = [7]
    elif dir == "stop":
        dir = [3,4]
    else:
        dir = list(range(num_pixels))
    while True:
        for i in dir:
            pixels[i] = (255, 0, 0)
        pixels.show()
        time.sleep(.5)
        for i in dir:    
            pixels[i]= (0,0,0)
        pixels.show()
        time.sleep(.5)
def forward(turndeg=0):
        pwm.set_pwm(2,0,turn(turndeg))
        pwm.set_pwm(0,0,servo_min)
        pwm.set_pwm(1,0,servo_max)
def backward(turndeg=0):
        pwm.set_pwm(2,0,turn(turndeg))
        pwm.set_pwm(0,0,servo_max)
        pwm.set_pwm(1,0,servo_min)
def stop(turndeg=0,isstop=True):
        pwm.set_pwm(2,0,turn(turndeg))
        pwm.set_pwm(0,1,0)
        pwm.set_pwm(1,1,0)

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
            stop(turndeg=request.form["turndeg"])
            return("stopping")
    else:
        return("still alive")
    
try :
    app.run(host='0.0.0.0')
finally:
    pwm.set_all_pwm(1,0)