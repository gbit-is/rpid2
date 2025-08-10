#!/usr/bin/env python3
import evdev
import sys
import time
from evdev import InputDevice, list_devices, categorize, ecodes
from common import *


gamepad_hints = config.get("joystick","name_hint")
gamepad_hints = gamepad_hints.split(",")

def find_gamepad(name_hints):

	devices = [InputDevice(path) for path in list_devices()]
	for device in devices:
		for name_hint in name_hints:
			if name_hint.lower() in device.name.lower():
				print(f"Found gamepad: {device.name} at {device.path}")
				return device, name_hint
		return None, None

def list_gamepads():
	devices = [InputDevice(path) for path in list_devices()]
	print("Devices found:")
	for device in devices:
		print(device.name)


def read_gamepad_loop():
	gamepad = None
	axis_state = { }
	while True:
		if gamepad is None:
			gamepad,name_hint = find_gamepad(gamepad_hints)
			if gamepad is None:
				time.sleep(1)
				continue
			gamepad.grab() 

		try:
			for event in gamepad.read_loop():
				if event.type == ecodes.EV_ABS:
					axis_state[event.code] = event.value





				elif event.type == ecodes.EV_KEY:
					print(categorize(event))

		except (OSError, IOError):
			print("Gamepad disconnected.")
			gamepad = None
			time.sleep(1)

if __name__ == "__main__":
	if "list" in "".join(sys.argv):
		list_gamepads()
		exit()	
	read_gamepad_loop()
