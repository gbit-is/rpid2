import sys
import time
import serial

from common import *
logger = get_logger("motor_server")


default_joystick_deadzone=20

def calculate_motors(direction,turn,deadzone=default_joystick_deadzone):

    def check_deadzone(value,threshold):
        if abs(value) < threshold:
            return 0
        else:
            return value

	
    direction = check_deadzone(direction, deadzone)
    turn = check_deadzone(turn, deadzone)

    left_motor = direction + turn
    right_motor = direction - turn

    left_motor = max(-256, min(256, left_motor))
    right_motor = max(-256, min(256, right_motor))

    return left_motor, right_motor

def initUART(config_section):
	serial_port = config.get(config_section,"serial_port")
	serial_baud = config.getint(config_section,"serial_baud")

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

