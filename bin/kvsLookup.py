
import sys 
from init import *
config = init_config()

kvs = init_kvs()

if len(sys.argv) != 2:
	print("provide key to look up")
	exit()

parameter = sys.argv[1]

if parameter not in kvs:
	print("key not found")
	exit()

value = kvs[parameter].decode()
print(value)
