import robohat
import time
import json
import os

settings = {}

def init():
    global settings
    if os.path.exists("johnny_settings.json"):
        settings = json.load(open("johnny_settings.json","r"))
    else:
        settings["tilt_centre"] = 0
        settings["rotation_angle"] = 0
        settings["speed"] = 100
        
    robohat.init()
    #robohat.startServos()
    #robohat.setServo(0,settings["tilt_centre"])
    robohat.setServo(1,settings["rotation_angle"])


def left_pulse():
    global settings
    
    # Check left
    robohat.setServo(1,settings["rotation_angle"] - 45)
    time.sleep(0.2)
    distance = int(robohat.getDistance())

    # Face forwards
    robohat.setServo(1,settings["rotation_angle"])

    return distance

def right_pulse():
    global settings
    
    # Check right
    robohat.setServo(1,settings["rotation_angle"] + 45)
    time.sleep(0.2)
    distance = int(robohat.getDistance())

    # Face forwards
    robohat.setServo(1,settings["rotation_angle"])

    return distance    


"""
# Return 0 if obstacle on left is further away
# Return 1 if obstacle on right is further away
"""
def side_distances():
    global settings

    left_distance = left_pulse()
    

    # Check right
    right_distance = right_pulse()

    
    # Decide left/Right
    if left_distance >= right_distance:
        return "Left"
    else:
        return "Right"
    

if __name__ == "__main__":
    init()

    try:
        while True:
            dist = int(robohat.getDistance())
            print("Distance: ", dist)
            left_ir = robohat.irLeft()
            right_ir = robohat.irRight()
            if not (left_ir or right_ir):
                if dist > 50:
                  robohat.forward(settings["speed"])
                  print("No obstacles in range to worry about")
                  time.sleep(0.5)
                elif dist > 10:
                    print("Getting close, speed is: ", int( (settings["speed"])*float(dist/50)))
                    robohat.forward(int( (settings["speed"])*float(dist/50)))
                    time.sleep(0.5)
                elif dist < 10:
                    print("I'm getting close, taking evasive action!")
                    if side_distances() == "Left":
                        print("Evading left!")
                        robohat.spinLeft(settings["speed"])
                    else:
                        print("Evading right!")
                        robohat.spinRight(settings["speed"])
                    time.sleep(0.5)
            else:
                if left_ir and not right_ir:
                    robohat.spinRight(settings["speed"])
                    print("Turning right to avoid obstacle")
                    time.sleep(0.5)
                elif not left_ir and right_ir:
                    robohat.spinLeft(settings["speed"])
                    print("Turning left to avoid obstacle")
                    time.sleep(0.5)
                else:
                    print("Which way to turn?")
                    if side_distances() == "Left":
                        robohat.spinLeft(settings["speed"])
                    else:
                        robohat.spinRight(settings["speed"])
                    time.sleep(1)

    except KeyboardInterrupt:
        print("No! No disassemble Number 5")
    finally:
        robohat.cleanup()
