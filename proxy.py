import zmq
import json 

def main():
    ctx = zmq.Context.instance()
    frontend = ctx.socket(zmq.PUB)
    frontend.bind("tcp://*:5557")
    backend = ctx.socket(zmq.SUB)
    backend.bind("tcp://*:5558")

    # Subscribe to publisher
    backend.setsockopt(zmq.SUBSCRIBE, b"")

    
    while True:
        try:
            msg = backend.recv_json()
            if 'lat' in msg and 'long' in msg and len(msg) == 2:
                frontend.send_json(msg)
            else:
                print("Incorrect data received, continuing..")

        except KeyboardInterrupt:
            print(" Interrupted by User")
            break
        except json.JSONDecodeError:
            print("Invalid message, continuing...")

if __name__ == '__main__':
    main()