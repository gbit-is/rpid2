#!/usr/bin/env python3
import sys
import time
import serial
import socket
import threading
from common import *
from json_db import *

logger = get_logger("motor_server")
limit_fetch_rate = 2 # secends between fetches


HOST = "0.0.0.0"
PORT = config.getint("ports","motor_server")

left_invert = config.getint("motors","left_drive_invert")
right_invert = config.getint("motors","right_drive_invert")

jdb = json_db()

class motor_limits_class():

	def __init__(self):
		self.update()

	def update(self):
		self.limit = ( fetch_motor_val() / 100 )



def fetch_motor_val():

	jdb.connection.sync()
	val = jdb.get("motors","speed","limit","value")[1]
	return val

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

	left_motor = left_motor * motor_limits.limit
	right_motor = right_motor * motor_limits.limit

	return left_motor, right_motor

def initUART(serial_port,serial_baud):

	logger.info("Connecting to mototor controller (UART)")


	uart_ready = False
	while not uart_ready:
		try:
			UART = serial.Serial (serial_port, serial_baud)    #Open port with baud rate
			uart_ready = True
			return UART

		except Exception as e:
			logger.error("Unable to connect UART\Error is:")
			logger.error(str(e))
			time.sleep(1)

def initUart_from_config(config_section):

	serial_port = config.get(config_section,"serial_port")
	serial_baud = config.getint(config_section,"serial_baud")

	return initUART(serial_port,serial_baud)


def send_drive_command(left_motor,right_motor,uart_interface):

	msg = "|" + str(left_motor) + "," + str(right_motor) + "@"
	uart_interface.write(msg.encode())
	


def parse_data(data):
	data = data.decode()
	if data.startswith("drive"):
		data = data.split(",")
		
		direction = float(data[1])
		turn = float(data[2])
		left_motor,right_motor = calculate_motors(direction,turn)
		send_drive_command(left_motor,right_motor,drive_motor_uart)
	
motor_limits = motor_limits_class()

t = threading.Thread(target=update_motor_val, args=(limit_fetch_rate,), daemon=True)
t.start()


while True:

	try:

		drive_motor_uart = initUart_from_config("motor_controller")
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
			s.bind((HOST, PORT))
			s.listen()
			conn, addr = s.accept()
			with conn:
				print(f"Connected by {addr}")
				while True:
					data = conn.recv(1024)
					if not data:
						break
					parse_data(data)
			
	except Exception as e:
		print("Error:")
		print(e)
