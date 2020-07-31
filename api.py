import time
import flask
import Adafruit_PCA9685
pwm = Adafruit_PCA9685.PCA9685()
# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
pwm.set_pwm_freq(60)
def forward():
        pwm.set_pwm(0,0,servo_min)
        pwm.set_pwm(1,0,servo_max)
def backward():
        pwm.set_pwm(0,0,servo_max)
        pwm.set_pwm(1,0,servo_min)
def stop():
        pwm.set_all_pwm(0,1)

app = flask.Flask(__name__)

@app.route('/move', methods=['GET','PUT'])
def move():
    if request.method == "PUT":
        if dir == "forward":
            forward()
            return("going forward")
        if dir == "backward":
            backward()
            return("going backward")
        else:
            stop()
            return("stopping")
    else:
        return("still alive")
    
app.run(host='0.0.0.0')