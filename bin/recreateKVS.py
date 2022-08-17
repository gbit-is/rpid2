
def createKVS():
	import dbm
	import configparser
	kvs = dbm.open('kvs', 'n')
	
	config = configparser.ConfigParser()
	config.read('../rpid2.conf')

	## Audio

	kvs["audio_loop_enabled"] = config["audio"]["loop"]	
	kvs["audio_loop_interval_low"] = config["audio"]["loop_interval_low"]
	kvs["audio_loop_interval_high"] = config["audio"]["loop_interval_high"]

	kvs["audio_song_enabled"] = config["audio"]["song_enabled"] 
	kvs["dome_manual_control"] = "True"




if __name__ == "__main__":
	from init import *
	config = init_config()
	createKVS()
