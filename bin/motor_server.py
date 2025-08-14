#!/usr/bin/env python3
import sys
import time
import serial
import socket

from common import *
logger = get_logger("motor_server")


HOST = "0.0.0.0"
PORT = config.getint("ports","motor_server")



def calculate_motors(direction,turn):

    left_motor = direction + turn
    right_motor = direction - turn

    left_motor = max(-256, min(256, left_motor))
    right_motor = max(-256, min(256, right_motor))

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
			logge.error(str(e))
			time.sleep(1)

def initUart_from_config(config_section):

	serial_port = config.get(config_section,"serial_port")
	serial_baud = config.getint(config_section,"serial_baud")

	return initUART(serial_port,serial_baud)


def send_drive_command(x,y,motor_uart):

	msg = "|" + str(left_motor) + "," + str(right_motor) + "@"


	
while True:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()
		conn, addr = s.accept()
		with conn:
			print(f"Connected by {addr}")
			while True:
				data = conn.recv(1024)
				if not data:
					break
				print(data)
			
