import requests
import time
time.sleep(10)
url = "http://192.168.3.127:5000/move"

pattern = [['backward','45'],['forward','45'],['backward','-45'],['forward','-45'],['stop','0']]
for move in pattern:
    payload = { 'dir' :move[0], 'turndeg':move[1] }
    res= requests.put(url, data=payload)    
    time.sleep(.5)