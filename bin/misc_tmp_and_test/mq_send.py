from paho.mqtt.client import Client, CallbackAPIVersion

# Use the correct enum, not an integer
#client = Client(callback_api_version=CallbackAPIVersion.v5)
client = Client(callback_api_version=CallbackAPIVersion.VERSION2)


client.connect("localhost", 1883)
client.publish("my/topic", "Hello with correct API version")
client.disconnect()
