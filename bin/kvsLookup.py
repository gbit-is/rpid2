
import sys 
from init import *
config = init_config()

kvs = init_kvs()

if len(sys.argv) != 2:
	print("List of keys: ")
	print("")

	keyLens = [ ]
	
	for key in kvs.keys():
		key = key.decode()
		keylen = len(key)
		keyLens.append(keylen)
	longestKey = max(keyLens)
	keyPad = longestKey + 5
		

	for key in kvs.keys():
		key = key.decode()
		value = kvs[key].decode()
		print(key.ljust(longestKey),value)
	print()

	exit()

parameter = sys.argv[1]

if parameter not in kvs:
	print("key not found")
	exit()

value = kvs[parameter].decode()
print(value)
