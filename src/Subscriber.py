import sys
import zmq
import time

ctx = zmq.Context()
sock = ctx.socket(zmq.SUB)


def subscribe(port):
    sock.connect("tcp://127.0.0.1:%d" % port)
    sock.subscribe("")  # Subscribe to all topics
    try:
        while True:
            msg = sock.recv_string()
            print("Received: %s" % msg)
    except KeyboardInterrupt as e:
        print("Proceso interrumpido ", e)
    sock.close()
    ctx.term()


if len(sys.argv) == 2:
    if sys.argv[1] == 'PH':
        subscribe(555)
    elif sys.argv[1] == 'T':
        subscribe(556)
    elif sys.argv[1] == 'O':
        subscribe(557)
    else:
        print("Non sensor %s aviable" % sys.argv[1])
else:
    print("No enough arguments")