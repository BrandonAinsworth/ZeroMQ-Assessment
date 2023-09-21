import time
import zmq
import random

def generate_random_lat_lon():
    
    lat = round(random.uniform(-90, 90),5)
    long = round(random.uniform(-180, 180),5)
    
    return {
        'lat': lat,
        'long': long
    }

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://localhost:5560")


try:
    while True:
        #  Wait for next request from client
            message = socket.recv()
            print(f"Received request: {message}")

            #  Do some 'work'
            time.sleep(5)
            random_lat_long = generate_random_lat_lon()
            #  Send reply back to client
            socket.send_json(random_lat_long)
    
#Handle Ctrl+C SIGINT from 0MQ Docs    
except KeyboardInterrupt:
    print(' Program Interrupted by User')
finally:
    socket.close()
    context.term()

