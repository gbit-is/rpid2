import sys
from init import *
config = init_config()
sys.path.append(init_libs())

import socket
import select
import os
import json

from motors import *

m1_a,m1_b,m2_a,m2_b = set_motor_gpios()


socketPath = config["sockets"]["main_motors"]


if os.path.exists(socketPath):
    os.remove(socketPath)

print("Opening socket...")

server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
server.bind(socketPath)
server.setblocking(0)

timeout_in_seconds = 0.1



def set_motors(command):
	print("foo")


noContact_count = 0
noContact_max = 30

while True:
	ready = select.select([server], [], [], timeout_in_seconds)
	if ready[0]:
		data = server.recv(4096).decode()
		#runMotor(-10,0,m1_a,m1_b,m2_a,m2_b)
		#time.sleep(2)
		#cleanup_motor_gpios(m1_a,m1_b,m2_a,m2_b)


		try:
			data = json.loads(data)
			#print(data)
			runMotor(data["X_axis"],data["Y_axis"],m1_a,m1_b,m2_a,m2_b)

		
		except Exception as e:
			print(" ")
			print(" ")
			print(" ")
			print("not json,stopping motors just in case")
			#cleanup_motor_gpios(m1_a,m1_b,m2_a,m2_b)
			print(data)
			print(e)
			print(" ")
			print(" ")
			print(" ")
			exit()

		noContact_count = 0
	else:
		noContact_count += 1
		if noContact_count > noContact_max:
			print("no contact recieved for "  + str(noContact_max) + " pulls")
			print("sending stop to motor")
			runMotor(0,0,m1_a,m1_b,m2_a,m2_b)
			noContact_count = 0

	#print(noContact_count)


server.close()
os.remove(socketPath)
cleanup_motor_gpios(m1_a,m1_b,m2_a,m2_b)
