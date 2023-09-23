import zmq

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
            frontend.send_json(msg)

        except KeyboardInterrupt:
            print(" Interrupted by User")
            break

if __name__ == '__main__':
    main()