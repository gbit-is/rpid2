import RPi.GPIO as GPIO
import time
from init import *
config = init_config()

power_multiplier = float(config["mainmotors"]["power_multiplier"])
steering_multiplier = float(config["mainmotors"]["steering_multiplier"])
speed_multiplier = float(config["mainmotors"]["speed_multiplier"])
rotate_multiplier = float(config["mainmotors"]["rotate_multiplier"])

DEBUG = False
DEBUG = True


def debug(msg):
	if DEBUG:
		print(msg)


def set_motor_gpios():

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(int(config["mainmotors"]["left_pin_pwm"]),GPIO.OUT)
	GPIO.setup(int(config["mainmotors"]["left_pin_dir"]),GPIO.OUT,initial=0)

	GPIO.setup(int(config["mainmotors"]["right_pin_pwm"]),GPIO.OUT)
	GPIO.setup(int(config["mainmotors"]["right_pin_dir"]),GPIO.OUT,initial=0)


	pwm_freq = int(config["mainmotors"]["pwm_freq"])

	left_motor_pwm  = GPIO.PWM(int(config["mainmotors"]["left_pin_pwm"]),pwm_freq)
	right_motor_pwm = GPIO.PWM(int(config["mainmotors"]["right_pin_pwm"]),pwm_freq)
	
	left_motor_dir  = int(config["mainmotors"]["left_pin_dir"])
	right_motor_dir = int(config["mainmotors"]["right_pin_dir"])


	left_motor_pwm.start(0)
	right_motor_pwm.start(0)
	

	return [ left_motor_pwm,left_motor_dir,right_motor_pwm,right_motor_dir ]

def cleanup_motor_gpios(motorPins):

	for pin in motorPins:
		pin.stop()

	GPIO.cleanup()


def runMotor(X_axis,Y_axis,motorPins):

	left_motor_pwm,left_motor_dir,right_motor_pwm,right_motor_dir = motorPins

	# X_axis (-100) - (+100) left to right, 0 = center
	# Y_axis (-100) - (+100) back to front, 0 = center

	X_axis_abs = ( abs(X_axis) * power_multiplier ) * steering_multiplier
	Y_axis_abs = ( abs(Y_axis) * power_multiplier ) * speed_multiplier
	
	if X_axis_abs < 0:
		X_axis_abs = 0
	elif X_axis_abs > 100:
		X_axis_abs = 100
	if Y_axis_abs < 0:
		Y_axis_abs = 0
	elif Y_axis_abs > 100:
		Y_axis_abs = 100

	if X_axis_abs + Y_axis_abs == 0:
		left_motor_pwm.ChangeDutyCycle(0)
		right_motor_pwm.ChangeDutyCycle(0)
		GPIO.output(left_motor_dir, 0)
		GPIO.output(right_motor_dir, 0)
		#debug("zero zero recieved. stopping motors")
		return


	if X_axis == 0:
		# no turning, just forwards/backwards
		if Y_axis > 0:
			left_direction = 1
			right_direction = 1
			debug("forwards")
		else:
			debug("backwards")
			left_direction = 0
			right_direction = 0

		GPIO.output(left_motor_dir, left_direction)
		GPIO.output(right_motor_dir, right_direction)
		left_motor_pwm.ChangeDutyCycle(Y_axis_abs)	
		right_motor_pwm.ChangeDutyCycle(Y_axis_abs)	

	elif Y_axis == 0:
		# rotate on the spot

		X_axis_abs = ( abs(X_axis) * power_multiplier ) * rotate_multiplier
		
		if X_axis > 0:
			debug("rotate right")
			left_direction = 1	
			right_direction = 0	

		else:	
			debug("rotate left")
			left_direction = 0	
			right_direction = 1	

		GPIO.output(left_motor_dir, left_direction)
		GPIO.output(right_motor_dir, right_direction)
		left_motor_pwm.ChangeDutyCycle(X_axis_abs)
		right_motor_pwm.ChangeDutyCycle(X_axis_abs)
	

	else:
		# complex movement
		debug("complex")
		if Y_axis > 0:
			debug("cplex: rightish")	
			leftTire_pwm_value = Y_axis_abs - X_axis_abs
			rightTire_pwm_value = Y_axis_abs
			if leftTire_pwm_value < 0:
				leftTire_pwm_value = 0
		else:
			debug("cplex: leftish")	
			rightTire_pwm_value = Y_axis_abs - X_axis_abs
			leftTire_pwm_value = Y_axis_abs
			if rightTire_pwm_value < 0:
				rightTire_pwm_value = 0
			
		if X_axis > 0:	
			left_direction = 1
			right_direction = 1
			debug("cplex: forwardish")

		else:
			debug("cplex: backwardish")
			left_direction = 0
			right_direction = 0

		GPIO.output(left_motor_dir, left_direction)
		GPIO.output(right_motor_dir, right_direction)
		left_motor_pwm.ChangeDutyCycle(leftTire_pwm_value)
		right_motor_pwm.ChangeDutyCycle(rightTire_pwm_value)


if __name__ == "__main__":

	motorPins = set_motor_gpios()
	try:
		runMotor(0,-30,motorPins)
	except Exception as e:
		print(e)
	time.sleep(0.5)
	cleanup_motor_gpios([motorPins[0],motorPins[2]])
