#!/usr/bin/env python3
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
from fastapi import Path as fastapi_path
from audio_server import list_files_for_ui
from mqttclient import *
from services_status import *



from common import *
from typing import Optional
from json_db import *
from gamepad_reciever import *


class c_socket():

	def __init__(self):
		self.socket = None
		self.create()
	def create(self):
		try:
			self.socket = create_socket()
		except Exception as e:
			print(e)
			self.socket = None
	def renew(self):
		self.__init__()

USE_STEAMDECK = False
if "steamdeck" in config:
	USE_STEAMDECK = True
	from gamepad_reciever import *
	m_socket = c_socket()
	axis = get_axis("steamdeck")

	keys = { }
	if config.has_section("steamdeck_keys"):
		for key in config["steamdeck_keys"]:
			keys[key] = config.get("steamdeck_keys",key)


USE_STEAMDECK = False

logger = get_logger("web-server")

jdb = json_db()
app = FastAPI()
try:
	mqc = mqttclient()
except Exception as e:
	logger.error("UNABLE TO CONNECT TO MQTT")
	logger.error(e)
	



app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def flatten_to_penultimate_level(d, parent_key=''):
	result = {}
	for k, v in d.items():
		full_key = f"{parent_key}.{k}" if parent_key else k
		if isinstance(v, dict) and all(isinstance(sub_v, dict) for sub_v in v.values()):
            		result.update(flatten_to_penultimate_level(v, full_key))
		else:
			if v["http_type"] is not None:
				result[full_key] = v
				#print(full_key,v)
	return result

def generate_controls_response():
	jdb.connection.sync() 
	data = jdb.get_all()
	#pprint(data)
	flat_dict = flatten_to_penultimate_level(data)
	return flat_dict



@app.get("/")
async def root():
	return RedirectResponse(url="/docs")


@app.get("/config/")
async def rd_config():
	return RedirectResponse(url="/docs")

@app.get("/config/list")
async def list_config():
	return JSONResponse(generate_controls_response())

@app.get("/config/get/{full_path:path}")
async def get_config_path(full_path: Optional[str] = ""):
	path_parts = tuple(filter(None, full_path.split("/")))

	if len(path_parts) == 0:
		return "no config specified"

	return jdb.get_value(*path_parts)

@app.post("/config/set/{full_path:path}")
async def set_config_path(
    full_path: str = fastapi_path(...),               # from the URL
    body: Optional[dict] = Body(None) 
):
	path_parts = tuple(filter(None, full_path.split("/")))	
	if len(path_parts) == 0:
		return "no key specified"
	if body is None:
		return "no body provided"

	if "value" not in body:
		return "invalid json, should be '{ 'value' : 'foo' }'"
	
	new_value = body["value"]

	current_value = jdb.get_value(*path_parts)
	if current_value is None:
		return "key does not exist"

	try:
		if current_value["type"] == "bool":
			if isinstance(new_value, bool):	
				pass
			elif new_value.lower() == "true":
				new_value = True
			elif new_value.strip().lower() == "false":
				new_value = False
			else:
				return "unable to process " + new_value + " as bool"
		elif current_value["type"] == "bool":
			new_value = str(new_value)

		elif current_value["type"] == "int":
			new_value = int(new_value)
		elif current_value["type"] == "float":
			new_value = float(new_value)
		else:
			return "don't know how to handle variable_type: " + current_value["type"]

	except Exception as e:
		return "Unable to process variable as: " + current_value["type"] + str(e)

	jdb.update(new_value,*path_parts)	
	
@app.get("/audio/list")
async def list_config():

	#audio_files_1 = [ "GENERATE","RANDOM"]	
	#audio_files_2 = list(list_audio_files())
	#audio_files = audio_files_1 + audio_files_2
	
	audio_files = { }
	audio_files["base"] = [ "GENERATE", "RANDOM"]

	audio_files.update(list_files_for_ui())
	
	return JSONResponse(audio_files)


@app.get("/services/status")
async def check_services():
	report = check_all_services()
	return JSONResponse(report)


@app.post("/mqtt/post/{topic}")
async def set_config_path(
    topic: str,
    body: Optional[str] = Body(None)
):

	topic = topic.replace("_","/")

	mqc = mqttclient()
	x = mqc.send(body,topic=topic)
	return "ACK"


@app.post("/drive")
async def drive(
    body: Optional[str] = Body(None)
):

	if not USE_STEAMDECK:
		return "steamdeck not configured"


	try:
		http_drive(body,axis,m_socket.socket)
	except Exception as e:
		print(e)
		m_socket.renew()
		http_drive(body,axis,m_socket.socket)

	body = json.loads(body)	
	for button in body["buttons"]:
		if button in keys:
			action,state = keys[button].split(":")
			pressed = body["buttons"][button]
			if pressed:
				pressed = "True"
			else:
				pressed = "False"
			if state.lower() == pressed.lower():
				if action == "mqtt":
					topic = config.get("steamdeck_mqtt",gamepad_key + "_topic")
					msg = config.get("steamdeck_mqtt",gamepad_key + "_message")
					mqc = mqttclient()
					mqc.send(msg,topic=topic)

	return "ACK"
