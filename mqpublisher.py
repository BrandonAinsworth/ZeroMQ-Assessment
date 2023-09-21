
#Author: Guillaume Aubert (gaubert) <guillaume(dot)aubert(at)gmail(dot)com>
   
import threading
import random
import zmq

def generate_random_lat_lon():
    
    lat = round(random.uniform(-90, 90),5)
    long = round(random.uniform(-180, 180),5)
    
    return {
        'lat': lat,
        'long': long
    }

def worker_routine(worker_url: str,
                   context: zmq.Context = None):
    """Worker routine"""
    context = context or zmq.Context.instance()

    # Socket to talk to dispatcher
    socket = context.socket(zmq.REP)
    socket.connect(worker_url)

    while True:
        

        string = socket.recv()
        print(f"Received request: {string} ")
        # Send reply back to client
        random_lat_long = generate_random_lat_lon()
        #  Send reply back to client
        socket.send_json(random_lat_long)
                
            

def main():
    
    try:
    
        """Server routine"""

        url_worker = "inproc://workers"
        url_client = "tcp://localhost:5560"

        # Prepare our context and sockets
        context = zmq.Context.instance()

        # Socket to talk to clients
        clients = context.socket(zmq.ROUTER)
        clients.connect(url_client)

        # Socket to talk to workers
        workers = context.socket(zmq.DEALER)
        workers.bind(url_worker)
        
        # Launch pool of worker threads
        for i in range(5):
            thread = threading.Thread(target=worker_routine, args=(url_worker,))
            thread.daemon = True
            thread.start()

        zmq.proxy(clients, workers)
    
    except KeyboardInterrupt:
        print(' Program Interrupted by User')
    finally:
        clients.close()
        workers.close()


if __name__ == "__main__":
    main()