import requests
import json
import time
import board
import neopixel
pixel_pin = board.D18
num_pixels = 16
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)
pixels.fill((255,0,0))
pixels.show()
time.sleep(2)
pixels.fill((0,0,0))
pixels.show()
print('turn signal ready')
req = requests.get('http://127.0.0.1:5000/move')
print(req.text)
def turnsignal(dir):
    if dir == "no":
        pixels.fill((0,0,0))
        pixels.show()
    elif dir == "left":
        dir = [7,8]
    elif dir == "right":
        dir = [0,15]
    elif dir == "stop":
        dir = [3,4,11,12]
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
        req = requests.get('http://127.0.0.1:5000/move')
        if req.text != dir:
                break
if True:
	while True:
		req = requests.get('http://127.0.0.1:5000/move')
		dir = req.text
		turnsignal(dir)
