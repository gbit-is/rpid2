import time
import serial
import os 


import serial.tools.list_ports
ports = serial.tools.list_ports.comports()


serial_devices_dir = "/dev/serial/by-id/"
all_serial_devices = os.listdir(serial_devices_dir)

MCUS = [ ]

for port, desc, hwid in sorted(ports):
	if "CDC2" in desc:
		details = hwid.split(" ")
		serial_nr = details[2].split("=")[1]
		#print(serial_nr)
		#MCUS.append(port)




all_serial_devices = [ "/dev/serial/by-id/usb-Raspberry_Pi_Pico_E660A49317642B24-if02"]

for device in all_serial_devices:
	device_path = os.path.join(serial_devices_dir,device)


	UART = serial.Serial(device_path,9600,timeout=1)
	#time.sleep(0.1)
	UART.write(b"whois")
	x = UART.read(64)
	print(device,x)

