#!/usr/bin/env python3
import time
import socket
from common import *
import Gamepad
from mqttclient import *
import select


logger = get_logger("gamepad_reciever")

logger.setLevel(logging.DEBUG)

# Set the host/port for the motor server, which talks to the motor controllers
HOST = "127.0.0.1"
PORT = config.getint("ports","motor_server")


# Get the static parameters from rpid2.conf
def get_axis(section):
	axis = { }
	axis["direction"] = config.getint(section,"direction")
	axis["turn"] = config.getint(section,"turn")
	axis["invert_direction"] =  config.getint(section,"invert_dir")
	axis["invert_turn"] =  config.getint(section,"invert_turn")
	axis["deadzone"] = config.getint(section,"deadzone")

	if config.has_option(section,"dome_right"):
		axis["dome"] = { }
		axis["dome"]["dome_right"] = config.getint(section,"dome_right")

		if config.has_option(section,"dome_left"):
			axis["dome"]["dome_left"] = config.getint(section,"dome_left")
		else:
			axis["dome"]["dome_left"] = None

		axis["dome"]["deadzone"] = config.getint(section,"dome_deadzone")
		if config.has_option(section,"dome_trigger"):
			axis["dome"]["trigger"] = config.getboolean(section,"dome_trigger")
		else:
			axis["dome"]["trigger"] = False


	return axis



# create a socket connection to the motor server
def create_socket():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	return s 



# Get the gamepad configuration and start the "daemon" that handles gamepad events
def init_gamepad():

	# initialise the gamepad class, if config["gamepad"]["gamepad_type"] is PS4, this is equivelant to "Gamepad.PS4"
	gamepad_type_name = config.get("gamepad","gamepad_type")
	gamepad_type = getattr(Gamepad, gamepad_type_name)


	# check if the gamepad is actually connected ..... 
	if not Gamepad.available():
		print('Please connect your gamepad...')
		while not Gamepad.available():
			print("waiting for gamepad")
			time.sleep(1.0)

	
	# Initialise the gamepad object
	gamepad = gamepad_type()
	print('Gamepad connected')
	gamepad.startBackgroundUpdates()
	return gamepad


# callback function when the drive axis change, only calls back with info of the axis being triggered
def drive(*args):

	# Here we just collect 2 values, how much back/forth movement should be done, how much left/right movement should be done
	# translating that to how much to drive each motor or if a motor is wired backwards or whatever, that is by design handled in the motor server itself


	# get status of all axis
	gamepad_data = gamepad.axisMap

	# Direction of travel (back or forth), is the gamepad axis, for direction, multiplied by 100
	# that is multiplied by the "invert_direction" number, which is either 1 for no or -1 for yes
	# the value we get from this, is then rounded to 2 decimals, which is more detail then we need
	direction = round( ( gamepad_data[axis["direction"]] * 100 ) * axis["invert_direction"],2 )

	# Direction of turning (left/right)  is the same logic are that for direction (back and forth)
	turn = round( ( gamepad_data[axis["turn"]] * 100 )  * axis["invert_turn"],2 )


	# check if the values are so close to zero, that they should be ignored
	if abs(direction) < axis["deadzone"]:
		direction = 0
	if abs(turn) < axis["deadzone"]:
		turn = 0
		
	# create the TCP packet to send to the motor server
	# the packet is by design small and simple "drive,100,0" is full speed forwards for example
	msg = "drive," + str(direction) + "," + str(turn)
	s.sendall(msg.encode())
	s.sendall(b"\n")


def http_drive(data,axis,s):

	data = json.loads(data)
	gamepad_data = data["axis"]



	direction = round( ( gamepad_data[str(axis["direction"])] * 100 ) * axis["invert_direction"],2 )
	turn = round( ( gamepad_data[str(axis["turn"])] * 100 )  * axis["invert_turn"],2 )
	if abs(direction) < axis["deadzone"]:
		direction = 0
	if abs(turn) < axis["deadzone"]:
		turn = 0

	if abs(direction) + abs(turn) > 0:
		msg = "drive," + str(direction) + "," + str(turn) + "\n"
		print("SENDING DRIIIIIVE")
		s.sendall(msg.encode())

	if "dome" in axis:
		dome_rotate = gamepad_data[str(axis["dome"]["dome_right"])]
		dome_rotate = dome_rotate * 100
		
		#if abs(dome_rotate) > axis["dome"]["deadzone"]:
		msg = "dome,rotate," + str(int(dome_rotate)) + "\n"
		s.sendall(msg.encode())
		print(msg)
	


def rotate_dome(*args):

	gamepad_data = gamepad.axisMap
	left_axis = axis["dome"]["dome_left"]
	right_axis = axis["dome"]["dome_right"]
	
	dome_left =  gamepad.axisMap[left_axis]
	dome_right =  gamepad.axisMap[right_axis]

	if axis["dome"]["trigger"]:
		dome_left  = ( dome_left + 1 ) / 2
		dome_right = ( dome_right + 1) / 2

	dome_left = dome_left * 100
	dome_right = dome_right * 100
	
	if dome_left < axis["dome"]["deadzone"]:
		dome_left = 0
	if dome_right < axis["dome"]["deadzone"]:
		dome_right = 0

	if dome_left > dome_right:
		dome_value = dome_left
	else:
		dome_value = dome_right * -1

	msg = "dome,rotate," + str(round(dome_value,0))
	print(msg)
	s.sendall(msg.encode())
	s.sendall(b"\n")

	

	
	

def catch_key(*args):

	key = args[1]
	value = args[0]
	
	key_data = keymap[str(key)]

	if key_data["key_type"] == "mqtt":
		topic = key_data["mqtt"]["topic"]
		msg = key_data["mqtt"]["msg"]
		
		mqc = mqttclient(topic=topic)
		mqc.send(msg)





# Manage gamepad, this function is what hooks up together the axis/keys and actions 
# and triggers a reset if the motor_server or gamepad_reciever goes down
def manage_gamepad(gamepad):
	
	
	gamepad.addAxisMovedHandler(axis["direction"],drive)
	gamepad.addAxisMovedHandler(axis["turn"],drive)

	if "dome" in axis:
		gamepad.addAxisMovedHandler(axis["dome"]["dome_left"],rotate_dome)
		gamepad.addAxisMovedHandler(axis["dome"]["dome_right"],rotate_dome)

	for gamepad_key in keymap:

		try:

			gamepad_key_value = keymap[gamepad_key]["key_value"]

			if gamepad_key_value ==	"Press":
				gamepad.addButtonPressedHandler(gamepad_key,catch_key)
			elif gamepad_key_value == "Release":
				gamepad.addButtonReleasedHandler(gamepad_key,catch_key)
			elif gamepad_key_value == "Change":
				gamepad.addButtonChangedHandler(gamepad_key,catch_key)
		except Exception as e:
			logger.error("Unable to assign handler to key: " + gamepad_key)
			logger.error(e)
	
		

	gamepad_connected = True
	socket_connected = True

	while gamepad_connected and socket_connected:

		gamepad_connected = gamepad.isConnected()
		try:
			s.sendall(b"ping")
		except socket.error as e:
			logger.error("Socket disconnected(socket.error)")
			logger.error(e)
			socket_connected = False
		except Exception as e:
			logger.error("Socket disconnected(generic exception)")
			logger.error(e)
			socket_connected = False

		time.sleep(1)
	raise Exception("manage gamepad crashed")


def print_err(e):
	logger.error("Unable to connect to motor server")
	logger.error(e)
	



keymap = { }

for gamepad_key in config["gamepad_keys"]:
	gamepad_key_data = config.get("gamepad_keys",gamepad_key)
	gamepad_key_data = gamepad_key_data.split(":")
	gamepad_key_type = gamepad_key_data[0]
	gamepad_key_value = gamepad_key_data[1]

	keymap[gamepad_key] = { }
	keymap[gamepad_key]["key_type"] = gamepad_key_type 
	keymap[gamepad_key]["key_value"] = gamepad_key_value

	if gamepad_key_type == "mqtt":
		try:
			keymap[gamepad_key]["mqtt"] = { }

			topic = config.get("gamepad_mqtt",gamepad_key + "_topic")
			msg = config.get("gamepad_mqtt",gamepad_key + "_message")

			keymap[gamepad_key]["mqtt"]["topic"] = topic
			keymap[gamepad_key]["mqtt"]["msg"] = msg
		except Exception as e:
			logger.error("Unable to configure key:" + gamepad_key)
			logger.error(e)



if __name__ == "__main__":
	axis = get_axis("gamepad")

	while True:

		socket_ready = False
		error_count=0
		max_error_count=10
		error_interval_count=0	
		error_interval_print=10

		while not socket_ready:
			try:
				s = create_socket()
				socket_ready = True
				print("Connected to motor server")
			except Exception as e:
				if error_count > max_error_count:
					if error_interval_count == error_interval_print:
						print_err(e)
						error_interval_count=0
					else:
						error_interval_count += 1				


				else:
					print_err(e)
				
				time.sleep(1)
				error_count += 1

		s_time = time.time()
		try:
			gamepad = init_gamepad()
			manage_gamepad(gamepad)
		except Exception as e:
			logger.error("manage gamepad loop went down with error:")
			logger.error(e)


			e_time = time.time()
			if e_time < 10:
				time.sleep(2)

		
