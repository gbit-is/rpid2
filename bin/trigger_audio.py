from common import *
from mqttclient import *



topic = config.get("mqtt_topics","audio_server")
msg = "play:RANDOM"
msg = "play:43SENT12"


mqc = mqttclient(topic=topic)
mqc.send(msg)
