# Pathological publisher
# Tests multiple publishers

import time
import zmq
import random
import sys

def generate_random_lat_lon():
    
    lat = round(random.uniform(-90, 90),5)
    long = round(random.uniform(-180, 180),5)
    
    return {
        'lat': lat,
        'long': long
    }

def main(testing=False):
    ctx = zmq.Context.instance()
    publisher = ctx.socket(zmq.PUB)
    publisher.connect("tcp://localhost:5558")
    test_iteration = 0
    
    while True:
        if testing and test_iteration >= 5:
            publisher.close()
            break
        
        # Send one random update per second
        try:
            time.sleep(1)
            latlong = generate_random_lat_lon()
            publisher.send_json(latlong)
            if testing:
                test_iteration += 1
        except KeyboardInterrupt:
            print (" Publisher Interrupted by User")
            publisher.close()
            break

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        main(testing=True)
    else:
        main()
