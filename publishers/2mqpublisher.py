#   Author of Paranoid Pirate Worker: Daniel Lundin <dln(at)eintr(dot)org>

from random import randint
import time
import random
import zmq
import json
import logging


def generate_random_lat_lon():
    
    lat = round(random.uniform(-90, 90),5)
    long = round(random.uniform(-180, 180),5)
    
    return {
        'lat': lat,
        'long': long
    }

HEARTBEAT_LIVENESS = 3
HEARTBEAT_INTERVAL = 1
INTERVAL_INIT = 1
INTERVAL_MAX = 32

#  Paranoid Pirate Protocol constants
PPP_READY = b"\x01"      # Signals worker is ready
PPP_HEARTBEAT = b"\x02"  # Signals worker heartbeat

def worker_socket(context, poller):
    """Helper function that returns a new configured socket
       connected to the Paranoid Pirate queue"""
    worker = context.socket(zmq.DEALER) # DEALER
    identity = b"%04X-%04X" % (randint(0, 0x10000), randint(0, 0x10000))
    worker.setsockopt(zmq.IDENTITY, identity)
    poller.register(worker, zmq.POLLIN)
    worker.connect("tcp://localhost:5556")
    worker.send(PPP_READY)
    return worker


context = zmq.Context(1)
poller = zmq.Poller()

liveness = HEARTBEAT_LIVENESS
interval = INTERVAL_INIT

heartbeat_at = time.time() + HEARTBEAT_INTERVAL

worker = worker_socket(context, poller)
cycles = 0


try:

    while True:
        socks = dict(poller.poll(HEARTBEAT_INTERVAL * 1000))

        # Handle worker activity on backend
        if socks.get(worker) == zmq.POLLIN:
            #  Get message
            #  - 3-part envelope + content -> request
            #  - 1-part HEARTBEAT -> heartbeat
            frames = worker.recv_multipart()
            if not frames:
                break # Interrupted

            if len(frames) == 3:
                # Simulate various problems, after a few cycles
                cycles += 1
                # if cycles > 3 and randint(0, 5) == 0:
                #     print("I: Simulating a crash")
                #     break
                # if cycles > 3 and randint(0, 5) == 0:
                #     print("I: Simulating CPU overload")
                #     time.sleep(3)
                
                latlonggen = generate_random_lat_lon()
                latlong = json.dumps(latlonggen, ensure_ascii=False).encode('utf8')
                worker.send_multipart([frames[0], b"", latlong])
                print("Message sent")
                liveness = HEARTBEAT_LIVENESS
                # Sleep to throttle message speed
                time.sleep(1)
            elif len(frames) == 1 and frames[0] == PPP_HEARTBEAT:
                # print("I: Queue heartbeat")
                liveness = HEARTBEAT_LIVENESS
            else:
                print("Invalid message: %s" % frames)
            interval = INTERVAL_INIT
        else:
            liveness -= 1
            if liveness == 0:
                print("Heartbeat failure, can't reach queue")
                print("Reconnecting in %0.2fs..." % interval)
                time.sleep(interval)
                # Close publisher if queue is unreachable at interval
                if interval == 4:
                    poller.unregister(worker)
                    worker.setsockopt(zmq.LINGER, 0)
                    worker.close()

                if interval < INTERVAL_MAX:
                    interval *= 2
                poller.unregister(worker)
                worker.setsockopt(zmq.LINGER, 0)
                worker.close()
                worker = worker_socket(context, poller)
                liveness = HEARTBEAT_LIVENESS
        if time.time() > heartbeat_at:
            heartbeat_at = time.time() + HEARTBEAT_INTERVAL
            # print("I: Worker heartbeat")
            worker.send(PPP_HEARTBEAT)
except KeyboardInterrupt:
    print(' Program Terminated by User')
except KeyError:
    print("Queue seems to be offline, abandoning")
finally:
    worker.close()