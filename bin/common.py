import os 					
import sys
import logging
import configparser
import json
from pathlib import Path

## JSON DB 
import ZODB, ZODB.FileStorage
import transaction
from persistent import Persistent
from persistent.mapping import PersistentMapping
from collections.abc import Mapping 


script_dir = os.path.dirname(os.path.abspath(__file__))
libs_path = os.path.abspath(os.path.join(script_dir, '..', 'libs'))

sys.path.append(libs_path)



logging.basicConfig(format="{asctime} - {name} - {levelname} - {message}",style="{",datefmt="%Y-%m-%d %H:%M",)




#logging.getLogger().setLevel(logging.DEBUG)

def pprint(msg):
	try:
		print(json.dumps(msg,indent=2,default=str))
	except:
		print(msg)



def get_dir_map():

        bin_dir = os.path.dirname(os.path.realpath(__file__))
        base_dir = os.path.abspath(os.path.join(bin_dir, os.pardir))

        dir_blacklist = [ "venv",".git","rpid2_v2-main" ]

        dir_map = { }
        for name in os.listdir(base_dir):
                full_path = os.path.join(base_dir,name)
                if os.path.isdir(full_path) and name not in dir_blacklist:
                        dir_map[name] = full_path

        return dir_map




def get_logger(logger_name):
	
	logger = logging.getLogger(logger_name)
	return logger


		


def get_dir_map():

	bin_dir = os.path.dirname(os.path.realpath(__file__))
	base_dir = os.path.abspath(os.path.join(bin_dir, os.pardir))

	dir_blacklist = [ "venv",".git","rpid2_v2-main" ]

	dir_map = { }
	for name in os.listdir(base_dir):
		full_path = os.path.join(base_dir,name)
		if os.path.isdir(full_path) and name not in dir_blacklist:
			dir_map[name] = full_path

	return dir_map
	



import configparser
config = configparser.ConfigParser(inline_comment_prefixes="#")
config.read('../etc/rpid2.conf')

if __name__ == "__main__":
	pass
