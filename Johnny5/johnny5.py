import robohat
import time

robohat.init()

speed = 80

try:
    robohat.startServos()
    #robohat.setServo(0,00)
    #robohat.setServo(0,35)
    while True:
        dist = int(robohat.getDistance())
        print("Distance: ", dist)
        left_ir = robohat.irLeft()
        right_ir = robohat.irRight()
        if not (left_ir or right_ir):
            if dist > 50:
              robohat.forward(speed)
              print("It's all so far away!")
              time.sleep(0.5)
            elif dist > 10:
                print("Getting close, speed is: ", int( (speed)*float(dist/50)))
                robohat.forward(int( (speed)*float(dist/50)))
                time.sleep(0.5)
            elif dist < 10:
                print("I'm getting close, taking evasive action!")
                robohat.spinLeft(speed)
                time.sleep(1)
        else:
            if left_ir and not right_ir:
                robohat.spinRight(speed)
                print("Turning right to avoid obstacle")
                time.sleep(0.5)
            elif not left_ir and right_ir:
                robohat.spinLeft(speed)
                print("Turning left to avoid obstacle")
                time.sleep(0.5)
            else:
                robohat.spinRight(speed)
                print("Turning around, way ahead is blocked")
                time.sleep(1)

except KeyboardInterrupt:
    print("No! No disassemble Number 5")
finally:
    robohat.cleanup()
