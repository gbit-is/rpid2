import sys
from init import *
config = init_config()
sys.path.append(init_libs())


import Gamepad
import time
import socket
import os 
import json




joystickSpeed = config["gamepad"]["joystickSpeed"]
joystickSteering = config["gamepad"]["joystickSteering"]

domeLeft = config["gamepad"]["domeLeft"]
domeRight = config["gamepad"]["domeRight"]

pollInterval = float(config["gamepad"]["pollInterval"])




deadZone = float(config["gamepad"]["deadZone"])
turnMultiplier = float(config["gamepad"]["turnMultiplier"])
steeringDivider = float(config["gamepad"]["steeringDivider"])
speedDivider = float(config["gamepad"]["speedDivider"])
mainMotorSocket = config["sockets"]["main_motors"]


speed = 0.0
steering = 0.0


def connectToSocket(socketPath):
	try:
		client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
		client.connect(socketPath)
		return client
	except Exception as e:
		print(e)
		return False

def sendToSocket(client,message):
	msg = json.dumps(message).encode()
	client.send(msg)


def initGamepad():

	gamepadType = Gamepad.PS4

	if not Gamepad.available():
        	print('Please connect your gamepad...')
        	while not Gamepad.available():
                	print("waiting for gamepad")
                	time.sleep(1.0)

	gamepad = gamepadType()
	print('Gamepad connected')
	gamepad.startBackgroundUpdates()


	return gamepad

def pollGamepad(gamepad):

	speed = ( gamepad.axis(joystickSpeed) * 100 ) * -1
	steering = gamepad.axis(joystickSteering) * 100
	dome_speed_l = gamepad.axis(domeLeft)
	dome_speed_r = gamepad.axis(domeRight)

	

	if abs(speed) < deadZone:
		speed = 0
	if abs(steering) < deadZone:
		steering = 0
	if ( dome_speed_l + dome_speed_r ) < -1.99:
		dome_speed = 0
	else:
		if dome_speed_l > -1 and dome_speed_r > -1:
			print("can't turn dome two ways at the same time")
			dome_speed = 0
		else:
			if dome_speed_l > -1:
				dome_axis = dome_speed_l
				dome_dir = 1
			else:
				dome_axis = dome_speed_r
				dome_dir = -1

			dome_speed = ((( (dome_axis + 1) / 2 ) * dome_dir ) * 100 )

	return speed, steering,dome_speed
	


def manage_gamepad():

	motorClient = False
	print("connecting to socket")
	while not motorClient:
		motorClient = connectToSocket(mainMotorSocket)
		if not motorClient:
			time.sleep(1)

	print("Connected to socket")

	gamepad = initGamepad()

	try:
		while gamepad.isConnected():
			axis = pollGamepad(gamepad)
			message = {
				"Y_axis" : axis[0],
				"X_axis" : axis[1]
			}
			if axis[2] != 0:
				message["D_axis"] = axis[2]

			try:
				sendToSocket(motorClient,message)
			except:
				motorClient = connectToSocket(mainMotorSocket)
			time.sleep(pollInterval)

	except KeyboardInterrupt:
		gamepad.disconnect()
if __name__ == "__main__":
	while True:
		manage_gamepad()
