#!/usr/bin/env python3
import os
import random
import time
import threading
import common
from json_db import *
from mqttclient import *
import pyvolume

#pyvolume.custom(percent=30)



audio_stop_events = {} 

NOSOUND = False
#NOSOUND = True

from common import *
logger = get_logger("audio_server")

logger.setLevel(logging.DEBUG)


jdb = json_db()




audio_dir = get_dir_map()["audio"]
alphabet_dir = os.path.join(audio_dir,"alphabet")
sounds_dir = os.path.join(audio_dir,"sounds")

alphabet_files = [os.path.join(alphabet_dir, file) for file in os.listdir(alphabet_dir)]

class volume_control_class():


	def __init__(self):
		self._get_vals()

	def _get_vals(self):
		jdb.connection.sync()
		self.enabled = jdb.get("audio","enabled","value")[1]
		self.volume_level = jdb.get("audio","volume","value")[1]
	def update(self):
		self.__init__()
		pyvolume.custom(self.volume_level)
		


volume_control = volume_control_class()

if not NOSOUND:
    if __name__ == "__main__":
        import pygame
        pygame.mixer.init()



def playSound(fileName):

	sound = pygame.mixer.Sound(fileName)
	playing = sound.play()
	while playing.get_busy():
		pygame.time.delay(10)

def generate_sound(low=3,high=10):
	randomCount = random.randint(low, high)
	print(low,high,randomCount)
	files = random.sample(alphabet_files,randomCount)
	word = ""
	for file in files:
		letter = file.split(".")[0].split("/")[-1]
		word += letter
	logger.debug("Word is: " + word)
	volume_control.update()
	if volume_control.enabled:
		logger.debug("Playing sound (generate_sound)")
		for file in files:
			playSound(file)

	else:
		logger.debug("not laying sound (generate_sound)")
def sound_loop_thread():

	isRunning = False
	loopThread = threading.Thread(target=sound_looper_proc, args=(),name="audio_loop_thread")

	for thread in threading.enumerate():
		if thread.name == "audio_loop_thread":
			isRunning = True
	if isRunning:
		logger.info("audio looper running")
		return 
	else:
		logger.info("starting audio looper")
		loopThread.start()


	


def sound_looper_proc():

    while True:
        jdb.connection.sync()
        if jdb.get("audio","loop","enabled","value")[1]:
            audio_loop_length_low = jdb.get("audio","loop","length","low","value")[1] 
            audio_loop_length_high = jdb.get("audio","loop","length","high","value")[1] 

            generate_sound(audio_loop_length_low,audio_loop_length_high)
		
            audio_loop_interval_low = jdb.get("audio","loop","interval","low","value")[1]
            audio_loop_interval_high = jdb.get("audio","loop","interval","high","value")[1]
		

            try:
                sleep_time = random.randint(audio_loop_interval_low,audio_loop_interval_high)
            except:
                logger.error("Failed to generate random time")
                sleep_time = 30
			

            logger.debug("Sleeping for: " + str(sleep_time) + " seconds")
            time.sleep(sleep_time)
        else:
            logger.debug("audio loop thread disabled")
            time.sleep(10)


def list_audio_files():

	
	all_files = []
	file_dir = { }
	for dirpath, dirnames, filenames in os.walk(sounds_dir):
		for filename in filenames:
			full_path = os.path.join(dirpath, filename)
			all_files.append(full_path)

	for file in all_files:
		file_title = file.split("/")[-1].split(".")[0].upper()
		file_dir[file_title] = file
	return file_dir

def list_files_for_ui():

	all_files = list_audio_files()

	file_dirs = { }

	


	for file in all_files:
		file_path = all_files[file]
		dir_name =  file_path.split("/")[-2]
		if dir_name not in file_dirs:
			file_dirs[dir_name] = [ ]
		file_dirs[dir_name].append(file)


	for directory in file_dirs:
		file_dirs[directory].sort()
		#file_dirs[directory] = file_dirs[directory].sort()


	return file_dirs


def play_audio_file(file_name,stop_event):

	file_dir = list_audio_files()
	file_name = file_name.upper()

  
	if file_name == "RANDOM":
		file_name = random.choice(list(file_dir))
	elif file_name == "GENERATE":
		generate_sound()
		return
	if file_name not in file_dir:
		logger.warning("Filename: " + file_name + " does not exist")
		return

	file_path = file_dir[file_name]
 
	volume_control.update()
	if volume_control.enabled:
		logger.debug("Playing sound (play_audio_file)")
		sound = pygame.mixer.Sound(file_path)
		playing = sound.play()
		while playing.get_busy():
			pygame.time.delay(10)
			if stop_event.is_set():
				sound.stop()
				break
	else:
		logger.debug("not playing sound (play_audio_file)")
				

def play_audio_file_wrapper(file_name):
    thread_name = "audio_play_thread"
    


    # If thread already exists, signal it to stop
    for thread in threading.enumerate():
        if thread.name == thread_name:
            logger.warning("Audio already playing. Stopping previous audio...")
            # Signal the existing thread to stop
            if thread_name in audio_stop_events:
                audio_stop_events[thread_name].set()
            thread.join()  # Wait for it to stop
            break  # There should only be one with this name

    # Create a new stop event for the new thread
    stop_event = threading.Event()
    audio_stop_events[thread_name] = stop_event

    # Start new thread
    play_audio_thread = threading.Thread(
        target=play_audio_file,
        args=(file_name, stop_event),
        name=thread_name,
	daemon=True
    )
    play_audio_thread.start()

		

def set_volume():

	volume = jdb.get("audio","volume","value")[1]
	pyvolume.custom(percent=volume)

def parse_mqtt_command(client, userdata, msg):
	
	print("MQTT RECIEVED")
	command = msg.payload.decode()
	if command.startswith("play"):
		file_name = command.split(":")[-1]
		play_audio_file_wrapper(file_name)
	else:
		logger.warning("Unknown MQTT command: " + command )
		


if __name__ == "__main__":
	
	
	topic = config.get("mqtt_topics","audio_server")

	mqc = mqttclient(topic=topic)
	mqc.listener(parse_mqtt_command)

	sound_loop_thread()
	
	while True:
		time.sleep(100)
			


