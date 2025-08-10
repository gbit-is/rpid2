from common import *
import serial
from common import init_common_config
import time
config = init_common_config()
kvs = init_kvs() # initalise KVS, make sure the KVS is populated 


print(config.sections())