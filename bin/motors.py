import RPi.GPIO as GPIO
import time
from init import *
config = init_config()

power_multiplier = float(config["mainmotors"]["power_multiplier"])
steering_multiplier = float(config["mainmotors"]["steering_multiplier"])
speed_multiplier = float(config["mainmotors"]["speed_multiplier"])
rotate_multiplier = float(config["mainmotors"]["rotate_multiplier"])


def set_motor_gpios():

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(int(config["mainmotors"]["left_pin_a"]),GPIO.OUT)
	GPIO.setup(int(config["mainmotors"]["left_pin_b"]),GPIO.OUT)
	GPIO.setup(int(config["mainmotors"]["right_pin_a"]),GPIO.OUT)
	GPIO.setup(int(config["mainmotors"]["right_pin_b"]),GPIO.OUT)


	pwm_freq = int(config["mainmotors"]["pwm_freq"])

	m1_a = GPIO.PWM(int(config["mainmotors"]["left_pin_a"]),pwm_freq)
	m1_b = GPIO.PWM(int(config["mainmotors"]["left_pin_b"]),pwm_freq)
	m2_a = GPIO.PWM(int(config["mainmotors"]["right_pin_a"]),pwm_freq)
	m2_b = GPIO.PWM(int(config["mainmotors"]["right_pin_b"]),pwm_freq)

	m1_a.start(0)
	m1_b.start(0)
	m2_a.start(0)
	m2_b.start(0)

	return m1_a,m1_b,m2_a,m2_b
def cleanup_motor_gpios(m1_a,m1_b,m2_a,m2_b):
	m1_a.stop()
	m1_b.stop()
	m2_a.stop()
	m2_b.stop()
	GPIO.cleanup()


def runMotor(X_axis,Y_axis,m1_a,m1_b,m2_a,m2_b):
	
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
		m1_a.ChangeDutyCycle(0)
		m1_b.ChangeDutyCycle(0)
		m2_a.ChangeDutyCycle(0)
		m2_b.ChangeDutyCycle(0)
		#print("zero zero recieved. stopping motors")
		return


	if X_axis == 0:
		# no turning, just forwards/backwards
		if Y_axis > 0:
			print("forwards")
			m1_a.ChangeDutyCycle(0)
			m1_b.ChangeDutyCycle(Y_axis_abs)
			m2_a.ChangeDutyCycle(0)
			m2_b.ChangeDutyCycle(Y_axis_abs)
		else:
			print("backwards")
			m1_a.ChangeDutyCycle(Y_axis_abs)
			m1_b.ChangeDutyCycle(0)
			m2_a.ChangeDutyCycle(Y_axis_abs)
			m2_b.ChangeDutyCycle(0)
	elif Y_axis == 0:
		# rotate on the spot

		X_axis_abs = ( abs(X_axis) * power_multiplier ) * rotate_multiplier
		
		if X_axis > 0:
			print("rotate right")
			m1_a.ChangeDutyCycle(X_axis_abs)
			m1_b.ChangeDutyCycle(0)

			m2_a.ChangeDutyCycle(0)
			m2_b.ChangeDutyCycle(X_axis_abs)
		else:	
			print("rotate left")
			m1_a.ChangeDutyCycle(0)
			m1_b.ChangeDutyCycle(X_axis_abs)
	
			m2_a.ChangeDutyCycle(X_axis_abs)
			m2_b.ChangeDutyCycle(0)
		
	# X_axis (-100) - (+100) left to right, 0 = center
	# Y_axis (-100) - (+100) back to front, 0 = center

	else:
		# complex movement
		print("complex")
		if Y_axis > 0:
			leftTire = Y_axis_abs - X_axis_abs
			rightTire = Y_axis_abs
			if leftTire < 0:
				leftTire = 0
		else:
			rightTire = Y_axis_abs - X_axis_abs
			leftTire = Y_axis_abs
			if rightTire < 0:
				rightTire = 0
			
		if X_axis > 0:	
			m1_a.ChangeDutyCycle(0)
			m1_b.ChangeDutyCycle(leftTire)
			m2_a.ChangeDutyCycle(0)
			m2_b.ChangeDutyCycle(rightTire)

		else:
			m1_a.ChangeDutyCycle(leftTire)
			m1_b.ChangeDutyCycle(0)
			m2_a.ChangeDutyCycle(rightTire)
			m2_b.ChangeDutyCycle(0)



if __name__ == "__main__":
	m1_a,m1_b,m2_a,m2_b = set_motor_gpios()
	runMotor(8.2,-7,m1_a,m1_b,m2_a,m2_b)
	time.sleep(2)
	cleanup_motor_gpios(m1_a,m1_b,m2_a,m2_b)
