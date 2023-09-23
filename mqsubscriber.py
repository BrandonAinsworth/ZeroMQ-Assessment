#Pathological subscriber


import math
import zmq
from dbmodule import write_radians_to_db

def convert_to_radians(message):
    lat_rad = round(((message['lat']) * math.pi / 180),5)
    long_rad = round(((message['long']) * math.pi / 180),5)
    
    return {
        'lat_rad': lat_rad,
        'long_rad': long_rad
    }

def main():
    ctx = zmq.Context.instance()
    subscriber = ctx.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5557")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"")

    while True: 
        try:
            data = subscriber.recv_json()
            converted_data = convert_to_radians(data)
            write_radians_to_db(converted_data)
            print(data)
        except KeyboardInterrupt:
            print(" Interrupted by User")
            break

if __name__ == '__main__':
    main()

