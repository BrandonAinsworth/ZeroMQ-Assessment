# Pathological publisher

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

def main():
    ctx = zmq.Context.instance()
    publisher = ctx.socket(zmq.PUB)
    publisher.connect("tcp://localhost:5558")

    while True:
        # Send one random update per second
        try:
            time.sleep(1)
            latlong = generate_random_lat_lon()
            publisher.send_json(latlong)
        except KeyboardInterrupt:
            print (" Interrupted by User")
            break

if __name__ == '__main__':
    main()
