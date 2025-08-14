#!/usr/bin/env python3
import time
import socket


from common import *

import Gamepad

HOST = "127.0.0.1"
PORT = config.getint("ports","motor_server")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

axis = { }
axis["direction"] = config.getint("gamepad","direction")
axis["turn"] = config.getint("gamepad","turn")
axis["invert_direction"] =  config.getint("gamepad","invert_dir")
axis["invert_turn"] =  config.getint("gamepad","invert_turn")
axis["deadzone"] = config.getint("gamepad","deadzone")


def init_gamepad():

	gamepad_type_name = config.get("gamepad","gamepad_type")

	gamepad_type = getattr(Gamepad, gamepad_type_name)


	if not Gamepad.available():
		print('Please connect your gamepad...')
		while not Gamepad.available():
			print("waiting for gamepad")
			time.sleep(1.0)

	gamepad = gamepad_type()
	print('Gamepad connected')
	gamepad.startBackgroundUpdates()
	return gamepad


def drive(*args):

	gamepad_data = gamepad.axisMap
	direction = round( ( gamepad_data[axis["direction"]] * 100 ) * axis["invert_direction"],2 )
	turn = round( ( gamepad_data[axis["turn"]] * 100 )  * axis["invert_turn"],2 )


	if abs(direction) < axis["deadzone"]:
		direction = 0
	if abs(turn) < axis["deadzone"]:
		turn = 0
		
	msg = "drive," + str(direction) + "," + str(turn)
	print(msg)
	s.sendall(msg.encode())

	
	


	
	


def manage_gamepad(gamepad):
	
	
	gamepad.addAxisMovedHandler(axis["direction"],drive)
	gamepad.addAxisMovedHandler(axis["turn"],drive)


gamepad = init_gamepad()
manage_gamepad(gamepad)
