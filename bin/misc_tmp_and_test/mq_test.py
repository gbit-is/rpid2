import paho.mqtt.client as mqtt

# Callback: called when connection is established
def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe("my/topic")  # Subscribe to the topic

# Callback: called when a message is received
def on_message(client, userdata, msg):
    print(f"Message received on topic {msg.topic}: {msg.payload.decode()}")

# Create MQTT client
client = mqtt.Client()

# Set callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to broker (no SSL or auth)
client.connect("localhost", 1883, 60)

# Start loop — non-blocking background loop
client.loop_start()

# Optionally block forever
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting...")
    client.loop_stop()
    client.disconnect()

