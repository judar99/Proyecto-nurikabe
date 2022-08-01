import sys
import zmq
import time
import random as rand


ctx = zmq.Context()
sock = ctx.socket(zmq.PUB)

def randomNumber(inf, sup, stat):
    randgen = lambda minval, maxval: round(minval + (maxval - minval) * rand.random(), 2)
    if stat == ["A"]:
        return randgen(inf, sup)
    elif stat == ["F"]:
        return rand.choice([randgen(0, inf), randgen(sup, abs(2 * sup))])
    else:
        return -randgen(0, 100)


class Publisher:
    def __init__(self, step, weights):
        self.step = step
        self.weights = weights.copy()

    def publish(self, inf, sup):
        try:
            while True:
                number = randomNumber(inf, sup, rand.choices(["A", "F", "E"], self.weights))
                sock.send_string("{}".format(number))
                print("Send {}".format(number))
                time.sleep(self.step)
        except KeyboardInterrupt as e:
            print("Proceso interrumpido ", e)
        sock.close()
        ctx.term()


class Sensor(Publisher):
    def __init__(self, arguments):
        step = arguments[0]
        filename = arguments[1]
        porc = open("conf/%s" % filename, "r").readlines()
        super().__init__(int(step), [100 * float(x.strip()) for x in porc])


if len(sys.argv) == 4:
    sensor = Sensor(sys.argv[2:])
    if sys.argv[1] == 'PH':
        sock.bind("tcp://*:555")
        sensor.publish(6,8)
    elif sys.argv[1] == 'T':
        sock.bind("tcp://*:556")
        sensor.publish(68, 89)
    elif sys.argv[1] == 'O':
        sock.bind("tcp://*:557")
        sensor.publish(2, 11)
    else:
        print("Non sensor %s aviable" % sys.argv[1])
else:
    print("No enough arguments")