import robohat
import time

robohat.init()

speed = 80

try:
    while True:
        dist = int(robohat.getDistance())
        print "Distance: ", dist
        left_ir = robohat.irLeft()
        right_ir = robohat.irRight()
        if not (left_ir or right_ir):
            if dist > 100:
              robohat.forward(speed)
              print "It's all so far away!"
              time.sleep(0.5)
            elif dist > 10:
                print "Getting close, speed is: ", (speed)/(dist)
                robohat.forward((speed)/dist)
                time.sleep(0.5)
            elif dist < 10:
                robohat.spinLeft(speed)
                time.sleep(1)
        else:
            if left_ir and not right_ir:
                robohat.spinRight(speed)
                time.sleep(0.5)
            elif not left_ir and right_ir:
                robohat.spinLeft(speed)
                time.sleep(0.5)
            else:
                robohat.spinRight(speed)
                time.sleep(1)

except KeyboardInterrupt:
    print "No! No disassemble Number 5"
