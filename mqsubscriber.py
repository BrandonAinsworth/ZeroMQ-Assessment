#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import math
context = zmq.Context()

#  Socket to talk to server
print("Connecting to 0MQ publisher…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

def convert_to_radians(message):
    lat_rad = round(((message['lat']) * math.pi / 180),5)
    long_rad = round(((message['long']) * math.pi / 180),5)
    
    return {
        'lat_rad': lat_rad,
        'long_rad': long_rad
    }
try:
#  Do 10 requests, waiting each time for a response
    for request in range(10):
        print(f"Sending request {request} …")
        socket.send(b"Latitude and longitude please!")

        #  Get the reply.
        message = socket.recv_json()
        print(f"Received reply {request} , {message} ")
        print(convert_to_radians(message))
        
#Handle Ctrl+C SIGINT from 0MQ Docs    
except KeyboardInterrupt:
    print(' Program Interrupted by User')
finally:
    socket.close()
    context.term()
