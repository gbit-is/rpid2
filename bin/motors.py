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

	GPIO.setup(int(config["domemotor"]["dome_motor_pwm"]),GPIO.OUT)
	GPIO.setup(int(config["domemotor"]["dome_motor_dir"]),GPIO.OUT,initial=0)


	pwm_freq = int(config["mainmotors"]["pwm_freq"])

	left_motor_pwm  = GPIO.PWM(int(config["mainmotors"]["left_pin_pwm"]),pwm_freq)
	right_motor_pwm = GPIO.PWM(int(config["mainmotors"]["right_pin_pwm"]),pwm_freq)
	dome_motor_pwm  = GPIO.PWM(int(config["domemotor"]["dome_motor_pwm"]),pwm_freq)
	
	left_motor_dir  = int(config["mainmotors"]["left_pin_dir"])
	right_motor_dir = int(config["mainmotors"]["right_pin_dir"])
	dome_motor_dir  = int(config["domemotor"]["dome_motor_dir"])


	left_motor_pwm.start(0)
	right_motor_pwm.start(0)
	dome_motor_pwm.start(0)
	

	return [ left_motor_pwm,left_motor_dir,right_motor_pwm,right_motor_dir,dome_motor_pwm,dome_motor_dir ]

def cleanup_motor_gpios(motorPins):

	for pin in motorPins:
		pin.stop()

	GPIO.cleanup()


def runMotor(axis_info,motorPins):

	left_motor_pwm,left_motor_dir,right_motor_pwm,right_motor_dir,dome_motor_pwm,dome_motor_dir = motorPins

	if "X_axis" in axis_info:
		X_axis = axis_info["X_axis"]
		Y_axis = axis_info["Y_axis"]


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
		print(Y_axis_abs)

		if X_axis_abs + Y_axis_abs == 0:
			debug("not moving")
			left_motor_pwm.ChangeDutyCycle(0)
			right_motor_pwm.ChangeDutyCycle(0)
			GPIO.output(left_motor_dir, 0)
			GPIO.output(right_motor_dir, 0)
			


		elif X_axis == 0:
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

	if "D_axis" in axis_info:
		D_axis = axis_info["D_axis"]
                #X_axis_abs = ( abs(X_axis) * power_multiplier ) * steering_multiplier
		D_axis_abs = abs(D_axis)
		if D_axis > 0:
			print("dome right")
			dome_direction = 1
		else:
			print("dome left")
			dome_direction = 0

		GPIO.output(dome_motor_dir,dome_direction)
		dome_motor_pwm.ChangeDutyCycle(D_axis_abs)


		


if __name__ == "__main__":
	axis_info = {'Y_axis': 0, 'X_axis': 0, 'D_axis': 30}
	#axis_info = {'Y_axis': 20, 'X_axis': 0}

	motorPins = set_motor_gpios()
	try:
		runMotor(axis_info,motorPins)
	except Exception as e:
		print(e)
		print(":(")
	time.sleep(0.5)
	cleanup_motor_gpios([motorPins[0],motorPins[2],motorPins[4]])
