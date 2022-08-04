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
pollInterval = float(config["gamepad"]["pollInterval"])

deadZone = float(config["gamepad"]["deadZone"])
turnMultiplier = float(config["gamepad"]["turnMultiplier"])
steeringDivider = float(config["gamepad"]["steeringDivider"])
speedDivider = float(config["gamepad"]["speedDivider"])
socketPath = config["sockets"]["main_motors"]


speed = 0.0
steering = 0.0


def connectToSocket():
	try:
		client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
		client.connect(socketPath)
		return client
	except Exception as e:
		print(e)
		return False

def sendToSocket(client,message):
	#print(message)
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

	if abs(speed) < deadZone:
		speed = 0
	if abs(steering) < deadZone:
		steering = 0
	return speed, steering
	


if __name__ == "__main__":

	client = False
	print("connecting to socket")
	while not client:
		client = connectToSocket()
		if not client:
			time.sleep(1)

	print("Connected to socket")

	gamepad = initGamepad()

	try:
		while gamepad.isConnected():
			axis = pollGamepad(gamepad)
			message = {
				"X_axis" : axis[1],
				"Y_axis" : axis[0]
			}
			try:
				sendToSocket(client,message)
			except:
				client = connectToSocket()
			time.sleep(pollInterval)

	except KeyboardInterrupt:
		gamepad.disconnect()
