#!/usr/bin/env python3
import sys
import time
import serial

from common import *


import Gamepad

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def initGamepad():

	gamepadType = Gamepad.Xbox360


	if not Gamepad.available():
        	print('Please connect your gamepad...')
        	while not Gamepad.available():
                	print("waiting for gamepad")
                	time.sleep(1.0)

	gamepad = gamepadType()
	print('Gamepad connected')
	gamepad.startBackgroundUpdates()

	return gamepad


def manage_gamepad(print_axis,print_keys):


	gamepad = initGamepad()



	#x = gamepad.movedEventMap
	#print(x)



	while True:
		axis_data = gamepad.axisMap	
		key_data = gamepad.pressedMap
			
		if print_keys:

			for key in key_data:
				key_val = key_data[key]
			
				if key_val:
					print(bcolors.OKGREEN + str(key).ljust(4) + bcolors.ENDC, end="")
				else:
					print(bcolors.OKBLUE + str(key).ljust(4) + bcolors.ENDC, end="")
			print()

		if print_axis:
			for axis in axis_data:
				axis_num = axis_data[axis]
				axis_num = round(axis_num,2)
				print(bcolors.OKBLUE + str(axis).ljust(2) + bcolors.ENDC +  str(axis_num).ljust(6),end="")
			print()
				
		time.sleep(0.5)


        
#print_axis = True
print_axis = False
print_keys = True
	

manage_gamepad(print_axis,print_keys)
