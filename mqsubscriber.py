#Pathological subscriber

import sys
import math
import zmq
import json
from dbmodule import write_radians_to_db

def convert_to_radians(message):
    lat_rad = round(((message['lat']) * math.pi / 180),5)
    long_rad = round(((message['long']) * math.pi / 180),5)
    
    return {
        'lat_rad': lat_rad,
        'long_rad': long_rad
    }

def main(testing=False):
    ctx = zmq.Context.instance()
    subscriber = ctx.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5557")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"")
    test_iteration = 0
    
    while True:
        if testing and test_iteration >= 5:
            subscriber.close()
            break
        try:
            data = subscriber.recv_json()

            if 'lat' in data and 'long' in data and len(data) == 2:
                converted_data = convert_to_radians(data)
                write_radians_to_db(converted_data)
                if testing:
                    test_iteration += 1
                print(data)
            else:
                print("Incorrect data received, continuing..")

        except KeyboardInterrupt:
            print(" Subscriber Interrupted by User")
            subscriber.close()
            break
        except json.JSONDecodeError:
            print("Invalid message, continuing...")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        main(testing=True)
    else:
        main()
