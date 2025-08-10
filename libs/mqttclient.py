from paho.mqtt.client import Client, CallbackAPIVersion


class mqttclient():
	
	
	defaults = {
		"host"		:	"localhost",
		"port"		:	1883,
		"topic"		:	"my/default",
		"api_version"	:	CallbackAPIVersion.VERSION2,


	}	

	def __init__(self,**kwargs):

		self.config = {**self.defaults, **kwargs}

		self.client = Client(callback_api_version=self.config["api_version"])
		self.client.connect("localhost", 1883)

	def send(self,message,topic=None):
		
		if topic is None:
			topic = self.config["topic"]
		print(topic,message)
		x = self.client.publish(topic, message)
		return x 

	def on_connect(self,client, userdata, flags, rc,huh):
		print("Connected with result code", rc)
		self.client.subscribe(self.config["topic"])

	def on_message(self,client, userdata, msg):
    		print(f"Message received on topic {msg.topic}: {msg.payload.decode()}")


	def listener(self,function_to_call):
		self.client.on_connect = self.on_connect
		self.client.on_message = function_to_call
		#self.on_message
		self.client.loop_start()

if __name__ == "__main__":

	def myfunc(client, userdata, msg):
		m = msg.payload.decode()
		t = msg.topic
		print(t,m)

	mqc = mqttclient(topic="/*")
	mqc.listener(myfunc)
	print("foo")
	import time
	time.sleep(60)
