import requests
import time
time.sleep(2)
ip = "192.168.1.242"
url = "http://" + ip + ":5000/move"

pattern = [['stop','90',2],['forward','90',.5],['stop','-90',2],['forward','-90',.5], ['stop','45',2],['forward','45',1],['backward','45',1],['stop','-45',2],['forward','-45',1],['backward','-45',1],['stop','0',0]]
for move in pattern:
    payload = { 'dir' :move[0], 'turndeg':move[1] }
    res= requests.put(url, data=payload)    
    time.sleep(move[2])
