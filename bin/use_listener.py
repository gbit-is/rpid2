#from common import *
import common



topic = "my/audio"
topic = "foo/bar"

from mqttclient import *
import time



def do_something(client, userdata, msg):
	print(msg.topic,msg.payload.decode())
	#print(client,userdata,msg)

mqc = mqttclient(topic=topic)
mqc.listener(do_something)


time.sleep(60)
