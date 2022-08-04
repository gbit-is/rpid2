
def createKVS():
	import dbm
	kvs = dbm.open('kvs', 'n')
	
	## Audio

	kvs["audio_loop_enabled"] = config["audio"]["loop"]	
	kvs["audio_loop_interval_low"] = config["audio"]["loop_interval_low"]
	kvs["audio_loop_interval_high"] = config["audio"]["loop_interval_high"]




if __name__ == "__main__":
	from init import *
	config = init_config()
	createKVS()
