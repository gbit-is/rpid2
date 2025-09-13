#!/usr/bin/env python3
import sys
import time
import serial
import socket
import threading
from common import *
from json_db import *
from motor_uart import *
import asyncio
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed  # base for OK+Error


logger = get_logger("motor_server")
logger.setLevel(logging.DEBUG)
limit_fetch_rate = 2 # secends between fetches


HOST = "0.0.0.0"
PORT = config.getint("ports","motor_server")

left_invert = config.getint("motors","left_drive_invert")
right_invert = config.getint("motors","right_drive_invert")

jdb = json_db()

class motor_limits_class():

	def __init__(self):
		self.limits = { }
		self.limits["drive"] = 0
		self.limits["dome"] = 0
		self.update()

	def update(self):
		limits = fetch_motor_val()
		self.limits["drive"] = limits[0] / 100
		self.limits["dome"] = limits[1] / 100



def fetch_motor_val():

	jdb.connection.sync()
	drive = jdb.get("motors","speed","limit","value")[1]
	dome = jdb.get("dome","speed","limit","value")[1]
	return drive, dome

def update_motor_val(interval):
	while True:
		motor_limits.update()
		time.sleep(interval)


def calculate_motors(direction,turn):

	left_motor = direction + turn
	right_motor = direction - turn

	left_motor = left_motor * left_invert
	right_motor = right_motor * right_invert

	left_motor = ( max(-100, min(100, left_motor)) ) / 100
	right_motor = ( max(-100, min(100, right_motor)) ) / 100

	left_motor = left_motor * motor_limits.limits["drive"]
	right_motor = right_motor * motor_limits.limits["drive"]

	return left_motor, right_motor

def send_drive_command(left_motor,right_motor):

	if motor_controllers["legs"]["enabled"]:
		msg = f"drive:{left_motor},{right_motor}\n"
		motor_controllers["legs"]["uart"].write(msg)
	else:
		logger.info("Main drive disabled")
	
def send_dome_command(rotate):

	if motor_controllers["dome"]["enabled"]:
		rotate = float(rotate) * motor_limits.limits["dome"]
		rotate = str(round(rotate / 100, 2))
		dome_msg = f"drive:{rotate}\n"
		motor_controllers["dome"]["uart"].write(dome_msg)
	else:
		logger.info("dome drive disabled")

def parse_data(data):

	try:
		if data.startswith("drive"):
			data = data.split(",")
			direction = float(data[1])
			turn = float(data[2])
			left_motor,right_motor = calculate_motors(direction,turn)
			send_drive_command(left_motor,right_motor)
			return
		elif data.startswith("ping"):
			logger.debug("pong")
			return
		elif data.startswith("dome"):
			data = data.split(",")
			if data[1] == "rotate":
				rotate = data[2]
				send_dome_command(rotate)
			return
	except Exception as e:
		logger.error("ERROR OCCURED IN PARSING COMMAND !!!")
		logger.error(e)
		logger.error(data)
		send_drive_command(0,0)
		send_dome_command(0)
	


async def handler(ws):
	try:
		async for msg in ws:       
			parse_data(msg)
	except ConnectionClosed:        
		logger.warning("conn close")

async def main():
	async with serve(handler, "", PORT) as server:
		await server.serve_forever()

motor_limits = motor_limits_class()

t = threading.Thread(target=update_motor_val, args=(limit_fetch_rate,), daemon=True)
t.start()


def init_controllers():
	#mcu_names = {'drive_controller': [{'version': 'v.0.9', 'id': '0123', 'path': '/dev/serial/by-id/usb-Raspberry_Pi_Pico_E660A49317642B24-if02'}]}
	mcu_names = {'dome_controller': [{'version': 'v.0.9', 'id': '0000', 'path': '/dev/serial/by-id/usb-Raspberry_Pi_Pico_E6616408436F8221-if02'}], 'drive_controller': [{'version': 'v.0.9', 'id': '0123', 'path': '/dev/serial/by-id/usb-Raspberry_Pi_Pico_E660A49317642B24-if02'}]}
	#mcu_names = scan_uarts()
	motor_controllers = { }

	controllers = config["motor_controllers"]
	for controller in controllers:
		motor_controllers[controller] = { }
		mcu_name = config.get("motor_controllers",controller)
		if "false" in mcu_name.lower():
			logger.warning(f"{controller} motor controller is disabled in config")
			motor_controllers[controller]["enabled"] = False
		elif mcu_name not in mcu_names:
			logger.warning(f"{controller} motor controller not connected")
			motor_controllers[controller]["enabled"] = False
		else:
			logger.info(f"{controller} motor controller found")
			motor_controllers[controller]["enabled"] = True
			motor_controllers[controller]["info"] = mcu_names[mcu_name]

	for controller in motor_controllers:
		c = motor_controllers[controller]
		if c["enabled"]:
			path = c["info"][0]["path"]
			motor_controllers[controller]["uart"] = motor_uart(path,9600,logger)
			
	
	return motor_controllers

if __name__ == "__main__":
		
	logger.info("initialising controllers")
	motor_controllers = init_controllers()
	asyncio.run(main())


