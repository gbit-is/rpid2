#!/usr/bin/env python3
import sys
import time
import serial

from common import *


import Gamepad



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

def initUART():
	serial_port = config.get("motor_controller","serial_port")
	serial_baud = config.getint("motor_controller","serial_baud")

	print("Connecting to mototor controller (UART)")

	uart_not_ready = True

	while uart_not_ready:
		try:
			UART = serial.Serial (serial_port, serial_baud)    #Open port with baud rate
			uart_not_ready = False
			
		except Exception as e:
			print("Unable to connect to motor controller (UART)")
			print("Error is:")
			print(e)
			print("will retry in N seconds")
			time.sleep(2)

	print("Connected to motor controller")
	return UART


	

def manage_gamepad():


	gamepad = initGamepad()



	old_axis_data = gamepad.axisMap	

	while True:
		axis_data = gamepad.axisMap	

		for a in axis_data:
			v = round(axis_data[a],2)
			print(a,str(v).ljust(8),end="")
			
		print()
			

		time.sleep(0.5)


        
		

manage_gamepad()
