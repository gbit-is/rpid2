#! /usr/bin/python3
import sys
import os 
import threading

rootDir = os.path.dirname(os.path.dirname(__file__))
libDir = rootDir + "/lib"
sys.path.append(libDir)

import Gamepad
import time
import configparser
from buttons import *
from sounds import *

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

config = configparser.ConfigParser()
config.read('../rpid2.conf')


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




gamepadType = Gamepad.PS4
joystickSpeed = config["gamepad"]["joystickSpeed"]
joystickSteering = config["gamepad"]["joystickSteering"]
pollInterval = float(config["gamepad"]["pollInterval"])

if not Gamepad.available():
	print('Please connect your gamepad...')
	while not Gamepad.available():
		print("waiting for gamepad")
		time.sleep(1.0)

gamepad = gamepadType()
print('Gamepad connected')


audioLoop = config.getboolean("audio","loop")
if audioLoop:
	audioLoopThread = threading.Thread(target=soundGen, args=(),name="audio_loop_thread")
	audioLoopThread.start()


deadZone = float(config["gamepad"]["deadZone"])
turnMultiplier = float(config["gamepad"]["turnMultiplier"])
steeringDivider = float(config["gamepad"]["steeringDivider"])
speedDivider = float(config["gamepad"]["speedDivider"])
motorRunning = True

# Set some initial state
speed = 0.0
steering = 0.0

# Start the background updating
gamepad.startBackgroundUpdates()


MOTORPRINT = config.getboolean("mainmotors","verbose")


gamepad.addButtonPressedHandler("CROSS", akey_pressed)
gamepad.addButtonPressedHandler("CIRCLE", bkey_pressed)
gamepad.addButtonPressedHandler("SQUARE", ykey_pressed)
gamepad.addButtonPressedHandler("TRIANGLE", xkey_pressed)



def motorControl(l_motor,r_motor,type):

	if type == "stop":
		m1_a.ChangeDutyCycle(0)
		m1_b.ChangeDutyCycle(0)
		m2_a.ChangeDutyCycle(0)
		m2_b.ChangeDutyCycle(0)
		return


	if l_motor[0] < 0:
		l_motor[0] = 0
	elif l_motor[0] > 100:
		l_motor[0] = 100

	if r_motor[0] < 0:
		r_motor[0] = 0
	elif r_motor[0] > 100:
		r_motor[0] = 100

	if l_motor[1] == "forward":
		m1_a.ChangeDutyCycle(0)
		m1_b.ChangeDutyCycle(l_motor[0])
	else:
		m1_a.ChangeDutyCycle(l_motor[0])
		m1_b.ChangeDutyCycle(0)

	if r_motor[1] == "forward":
		m2_a.ChangeDutyCycle(0)
		m2_b.ChangeDutyCycle(l_motor[0])
	else:
		m2_a.ChangeDutyCycle(l_motor[0])
		m2_b.ChangeDutyCycle(0)


	

	if MOTORPRINT:
		print("Motor".ljust(10) + "Direction".ljust(15) +"Speed".ljust(10) + type)
		print("Left".ljust(10) + l_motor[1].ljust(15) + str(int(l_motor[0])) + "%")
		print("Right".ljust(10) + r_motor[1].ljust(15) + str(int(r_motor[0])) + "%")
		#print("Right	" + r_motor[1] + "	" + str(r_motor[0]) + "%")
		print("")





# Joystick events handled in the background
try:
	while gamepad.isConnected():


		

		speed = ( gamepad.axis(joystickSpeed) * 100 ) * -1
		steering = gamepad.axis(joystickSteering) * 100
		
		#print(gamepad.axis(joystickSpeed))



		if abs(speed) < deadZone:
			speed = 0
		if abs(steering) < deadZone:
			steering = 0

		if abs(speed) + abs(steering) == 0:
			if motorRunning:
				print("stopping motors")
				motorControl("","","stop")
				motorRunning = False

		# steering is being performed
		else:
			steering = steering / steeringDivider
			speed = speed / speedDivider
			
			# just forward / backwards
			if steering == 0:
				if speed > 0:	
					direction = "forward"
				else:
					direction = "backward"
				speedAbs = abs(speed)
				motorRunning = True
				motorControl([speedAbs,direction],[speedAbs,direction],"fb")

			# just rotating
			elif speed == 0:
				
				steeringAbs = abs(steering)
				if steering > 0:
					motorRunning = True
					motorControl([steeringAbs,"forwardd"],[steeringAbs,"backward"],"rt")

				else:
					motorRunning = True
					motorControl([steeringAbs,"backward"],[steeringAbs,"forward"],"rt")
			else:
					steeringAbs = abs(steering)
					speedAbs = abs(speed)

					if speed > 0:
						direction = "forward"
					else:
						direction = "backward"

					mainTire = speedAbs
					turnTire = speedAbs - ( steeringAbs * turnMultiplier )

					if steering < 0:
						motorRunning = True
						motorControl([turnTire,direction],[mainTire,direction],"complex")
					else:
						motorRunning = True
						motorControl([mainTire,direction],[turnTire,direction],"complex")


					
				

			time.sleep(pollInterval)
except KeyboardInterrupt:
	gamepad.disconnect()
	m1_a.stop()
	m1_b.stop()
	m2_a.stop()
	m2_b.stop()
	GPIO.cleanup()
	exit()

		
finally:
	gamepad.disconnect()
	m1_a.stop()
	m1_b.stop()
	m2_a.stop()
	m2_b.stop()

	GPIO.cleanup()
	exit()
