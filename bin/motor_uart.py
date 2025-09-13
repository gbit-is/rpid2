import time
import serial
import os 

MCU_PATTERNS = [ "Raspberry_Pi_Pico" ]


class motor_uart ():


	reconnect_max = 5 
	
	def __init__(self,serial_port,serial_baud,logger):
		self.serial_port = serial_port
		self.serial_baud = serial_baud
		self.logger = logger
		self.connected = False
		self.connect()
	
	def connect(self):

		self.logger.info("Connecting to motor controller (UART)")
		retry_uart = True
		retry_count = 0
		while retry_uart:
			#self.logger.info("Trying to connect to " + name + "(" + str(retry_count) + "/" + str(self.reconnect_max) + ")")
			self.logger.info(f"Trying to connect to {self.serial_port} ({retry_count}/{self.reconnect_max})")
			try:
				UART = serial.Serial(self.serial_port, self.serial_baud) 
				retry_uart = False
				self.uart = UART
				self.conntected = True
				self.logger.info(f"Successfully connected to {self.serial_port}")
				self.enabled = True
				return True
			except Exception as e:
				#self.logger.error("Unable to connect " + name + " UART\nError is:")
				self.logger.error(f"Unable to connect to {self.serial_port} Error is:\n {e}")
				self.logger.error(str(e))
				retry_count += 1
				if retry_count >= self.reconnect_max:
					retry_uart = False
					self.logger.error("Giving up on UART for: " + name)
				else:
					time.sleep(1)
		self.connected = False
		self.uart = None
		return False

	def write(self,msg):
		if self.enabled:
			try:
				self.uart.write(msg.encode())
			except Exception as e:
				print(e)
		else:
			logger.warning("motor controller not enabled")



def scan_uarts():
	serial_devices_dir = "/dev/serial/by-id/"
	all_serial_devices = os.listdir(serial_devices_dir)

	MCUS = { }
	for device in all_serial_devices:
		device_path = os.path.join(serial_devices_dir,device)
		if any(sub in device_path for sub in MCU_PATTERNS):
			UART = serial.Serial(device_path,9600,timeout=1)
			time.sleep(0.1)
			UART.write(b"whois\n")
			res = UART.read(64)
			res = res.decode()
			if "version" in res:
				try:
					null, mcu_name, mcu_version, mcu_id  = res.split(":")
				except Exception as e:
					logger.error(f"Unable to split info from {device_path}")
					mcu_name = "error"
					mcu_version = "error"
					mcu_id = "error"

				if mcu_name not in MCUS:
					MCUS[mcu_name] = [ ]
				mcu_data = {
					"version" : mcu_version,
					"id"      : mcu_id,
					"path"    : device_path
				}
				MCUS[mcu_name].append(mcu_data)
				
	return MCUS



if __name__ == "__main__":
	print(scan_uarts())
