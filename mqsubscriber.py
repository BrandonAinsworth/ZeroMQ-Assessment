#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to 0MQ publisher…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

try:
#  Do 10 requests, waiting each time for a response
    for request in range(10):
        print(f"Sending request {request} …")
        socket.send(b"Latitude and longitude please!")

        #  Get the reply.
        message = socket.recv()
        print(f"Received reply {request} , {message} ")

        
#Handle Ctrl+C SIGINT from 0MQ Docs    
except KeyboardInterrupt:
    print(' Program Interrupted by User')
finally:
    socket.close()
    context.term()
