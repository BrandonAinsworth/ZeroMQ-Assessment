# import zmq
# import math
# from database.lat_long_db import write_radians_to_db
# import json

# context = zmq.Context()

# #  Socket to talk to server
# socket = context.socket(zmq.REQ)
# socket.connect("tcp://localhost:5555")

# poller = zmq.Poller()
# poller.register(socket, zmq.POLLIN)

# def convert_to_radians(message):
#     lat_rad = round(((message['lat']) * math.pi / 180),5)
#     long_rad = round(((message['long']) * math.pi / 180),5)
    
#     return {
#         'lat_rad': lat_rad,
#         'long_rad': long_rad
#     }
# try:
# #  Do 10 requests, waiting each time for a response
#     for request in range(100):
#         print(f"Sending request {request} …")
#         socket.send(b"Latitude and longitude please!")
        
#         #  Get the reply.
#         message = socket.recv()
#         message = message.decode()
#         print(f"Received reply {request} , {message} ")
#         message = json.loads(message)
#         converted_data = convert_to_radians(message)
#         write_radians_to_db(converted_data)
        
# except KeyboardInterrupt:
#     print(' Program Interrupted by User')
# finally:
#     socket.close()


#   Author of Lazy Pirate Client: Daniel Lundin <dln(at)eintr(dot)org>
#
import itertools
import logging
import math
import sys
import zmq
import json
from database.lat_long_db import write_radians_to_db

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

def convert_to_radians(message):
    lat_rad = round(((message['lat']) * math.pi / 180),5)
    long_rad = round(((message['long']) * math.pi / 180),5)
    
    return {
        'lat_rad': lat_rad,
        'long_rad': long_rad
    }

REQUEST_TIMEOUT = 3000
REQUEST_RETRIES = 3
SERVER_ENDPOINT = "tcp://localhost:5555"

context = zmq.Context()

logging.info("Connecting to queue..")
client = context.socket(zmq.REQ)
client.connect(SERVER_ENDPOINT)

try:

    for sequence in itertools.count():
        request = str(sequence).encode()
        logging.info("Sending (%s)", request)
        client.send(request)

        retries_left = REQUEST_RETRIES
        while True:
            if (client.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
                reply = client.recv()
                if int(request) == sequence:
                    logging.info("Server replied OK (%s)", reply)
                    reply = reply.decode()
                    print(f"Received reply {request} , {reply} ")
                    reply = json.loads(reply)
                    converted_data = convert_to_radians(reply)
                    write_radians_to_db(converted_data)
                    retries_left = REQUEST_RETRIES
                    break
                else:
                    logging.error("Malformed reply from queue: %s", reply)
                    continue

            retries_left -= 1
            logging.warning("No response from queue")
            # Socket is confused. Close and remove it.
            client.setsockopt(zmq.LINGER, 0)
            client.close()
            if retries_left == 0:
                logging.error("Queue seems to be offline, abandoning")
                # Abandoning, close socket and exit
                client.close()
                sys.exit()
                
            logging.info("Reconnecting to queue")
            # Create new connection
            client = context.socket(zmq.REQ)
            client.connect(SERVER_ENDPOINT)
            logging.info("Resending (%s)", request)
            client.send(request)
except KeyboardInterrupt:
    logging.error(' Program Interrupted by User')
finally:
    client.close()