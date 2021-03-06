import time, sys, math
import RPi.GPIO as GPIO
import robohat

wheel_enc = 15
segments = 36
start_time = time.time()

dist_meas = 0.00
km_per_hour = 0
rpm = 0
elapse = 0
pulse = 0
start_timer = time.time()

def init_interrupt():
	GPIO.add_event_detect(wheel_enc, GPIO.RISING, callback = calculate_elapse)#, bouncetime = 20)

def calculate_elapse(channel):
	print("pulse:", pulse)
	global pulse, start_timer, elapse	
	pulse += 1
	elapse = time.time() - start_timer
	start_timer = time.time()


def calculate_speed(r_cm):
	global pulse,elapse,rpm,dist_km,dist_meas,km_per_sec,km_per_hour
	if elapse !=0:                     # to avoid DivisionByZero error
		print("I think I've had", pulse//segments, "revolutions.")
		rpm = (elapse/20) * 60
		circ_cm = (2*math.pi)*r_cm         # calculate wheel circumference in CM
		dist_km = circ_cm/100000          # convert cm to km
		km_per_sec = dist_km / elapse /20     # calculate KM/sec
		km_per_hour = km_per_sec * 3600      # calculate KM/h
		dist_meas = (dist_km*pulse)*1000   # measure distance traverse in meter
		return rpm
	

if __name__ == "__main__":
	#GPIO.setmode(GPIO.BOARD)
	robohat.init()
	GPIO.setup(wheel_enc, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Left wheel encoder
	init_interrupt()
	speed = 10
	try:
		while pulse < segments:
			#print(pulse)
			#print("Speed: " + str(speed) +"\nSensor: " + str(wheel_speed))
			robohat.forward(speed)

		print("Stopping")
		robohat.stop()	       
	except KeyboardInterrupt:
		print("Shutting down")
	finally:
		robohat.cleanup()
