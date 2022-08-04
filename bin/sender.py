# -*- coding: utf-8 -*-
import socket
import os
import json


sockAddr = "/tmp/main_motor_socket"

print("Connecting...")
if os.path.exists(sockAddr):
	
	try:
	
		client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
		client.connect(sockAddr)
		#msg = "hello my foobar".encode()
		#m = { "hello" : "world"}
		m = {}
		m["X_axis"] = 5
		m["Y_axis"] = 0
		msg = json.dumps(m).encode()
		client.send(msg)
	except Exception as e:
		print("socket is dead")
		print(e)

else:
    print("Couldn't Connect!")
    print("Done")
