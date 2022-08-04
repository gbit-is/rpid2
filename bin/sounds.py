import os
import random
import time
import threading


NOSOUND = False
NOSOUND = True

from init import *
config = init_config()



rootDir = os.path.dirname(os.path.dirname(__file__))
soundDir = rootDir + "/sounds"




if not NOSOUND:
	import pygame
	pygame.mixer.init()

sounds = [ "a","b","c1","c","d","e","f","g1","g","h","i","j","k","l","m","n","o1","o","p","q","r","s1","s","t","u1","u","v","w","x","y","z" ]


def playSound(fileName):

	fullName = soundDir + "/" + fileName + ".wav"
	if not NOSOUND:
		sound = pygame.mixer.Sound(fullName)
		playing = sound.play()
		while playing.get_busy():
			pygame.time.delay(10)

def randomSound(low=3,high=10):
	randomCount = random.randint(low, high)
	files = random.sample(sounds,randomCount)
	print("Word is: " + ''.join(files))
	for file in files:
		playSound(file)



def sound_loop_thread():


	kvs = init_kvs()

	audio_loop_enabled = kvs["audio_loop_enabled"].decode()

	while audio_loop_enabled == "True":
		randomSound()
		kvs = init_kvs()
		
		audio_loop_interval_low = int(kvs["audio_loop_interval_low"].decode())
		audio_loop_interval_high = int(kvs["audio_loop_interval_high"].decode())

		sTime = random.randint(audio_loop_interval_low,audio_loop_interval_high)

		print("Sleeping for: " + str(sTime) + " seconds")
		time.sleep(sTime)
		audio_loop_enabled = kvs["audio_loop_enabled"].decode()

		

if __name__ == "__main__":

	while True:


		kvs = init_kvs()
		isRunning = False

	

		
	
		audio_loop_enabled = kvs["audio_loop_enabled"].decode()	
		if audio_loop_enabled == "True":
			sound_loop_thread()
	
		time.sleep(3)


