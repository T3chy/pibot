import requests
import json
import time
import board
import neopixel
pixel_pin = board.D18
num_pixels = 8
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)
req = requests.get('http://127.0.0.1:5000/')
print(req.json()['hello'])
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
    while True:
        for i in dir:
            pixels[i] = (255, 0, 0)
        pixels.show()
        time.sleep(.5)
        for i in dir:
            pixels[i]= (0,0,0)
        pixels.show()
        time.sleep(.5)
	req = requests.get('http://127.0.0.1:5000/')
	if req.json()['dir'] != dir:
		break
if __name__ == __main__:
	while True:
		req = requests.get('http://127.0.0.1:5000/')
		dir = req.json()['dir']
		turnsignal(dir)
