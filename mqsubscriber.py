import zmq
import math
from database.lat_long_db import write_radians_to_db
import json

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
    for request in range(100):
        print(f"Sending request {request} …")
        socket.send(b"Latitude and longitude please!")

        #  Get the reply.
        # message = socket.recv_json()
        message = socket.recv()
        message = message.decode()
        print(f"Received reply {request} , {message} ")
        message = json.loads(message)
        converted_data = convert_to_radians(message)
        write_radians_to_db(converted_data)
        
#Handle Ctrl+C SIGINT from 0MQ Docs    
except KeyboardInterrupt:
    print(' Program Interrupted by User')
finally:
    socket.close()
    context.term()
