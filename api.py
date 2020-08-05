import time
import flask
from flask import request
import Adafruit_PCA9685
import time
import board
import neopixel
pixel_pin = board.D18
num_pixels = 16
ORDER = neopixel.GRB
 
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)
pwm = Adafruit_PCA9685.PCA9685()
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
pwm.set_pwm_freq(60)
signal = ""
dir = ""
deg = ""
pixels.fill((255,0,0))
pixels.show()
def turn(degrees,isstop=False):
    degrees = float(degrees)
    if degrees == 0:
        dir = "no"
    elif abs(degrees) == degrees:
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
    pixels.fill((0,0,0))
    pixels.show()
def turnsignal(dir):
    if dir == "no":
        pixels.fill((0,0,0))
        pixels.show()
    elif dir == "left":
        dir = [0]
    elif dir == "right":
        dir = [7]
    elif dir == "stop":
        dir = [3,4]
    else:
        dir = list(range(num_pixels))
#    while True:
#        for i in dir:
#            pixels[i] = (255, 0, 0)
#        pixels.show()
#        time.sleep(.5)
#        for i in dir:    
#            pixels[i]= (0,0,0)
#        pixels.show()
#        time.sleep(.5)
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
    global dir
    global deg
    if request.method == "PUT":
        dir = request.form["dir"]
        deg = request.form['turndeg']
        if dir == "forward":
            forward(turndeg=deg)
            return("going forward")
        elif dir == "backward":
            backward(turndeg=deg)
            return("going backward")
        else:
            stop(turndeg=deg)
            return("stopping")
    else:
        deg = int(deg) if deg != "" else 0
        return "right" if deg > 0 else "left"
        #return{"alive":'yes', "dir":dir, 'turndeg':deg}
import subprocess
try:
    subprocess.Popen(["sudo", "python3", 'turnsignal.py'])
    dir = ""
    deg = ""
    app.run(host='0.0.0.0')
finally:
    pwm.set_all_pwm(1,0)
