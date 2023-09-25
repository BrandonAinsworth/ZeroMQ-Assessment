import zmq
import json 
import sys

def main(testing=False):
    ctx = zmq.Context.instance()
    frontend = ctx.socket(zmq.PUB)
    frontend.bind("tcp://*:5557")
    backend = ctx.socket(zmq.SUB)
    backend.bind("tcp://*:5558")
    test_iteration = 0
    # Subscribe to publisher
    backend.setsockopt(zmq.SUBSCRIBE, b"")

    
    while True:
        if testing and test_iteration >= 5:
            frontend.close()
            backend.close()
            break
        try:
            msg = backend.recv_json()
            if 'lat' in msg and 'long' in msg and len(msg) == 2:
                frontend.send_json(msg)
                if testing:
                    test_iteration += 1
            else:
                print("Incorrect data received, continuing..")

        except KeyboardInterrupt:
            print(" Proxy Interrupted by User")
            frontend.close()
            backend.close()
            break
        except json.JSONDecodeError:
            print("Invalid message, continuing...")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        main(testing=True)
    else:
        main()