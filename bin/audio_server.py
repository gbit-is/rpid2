import os
import random
import time
import threading


NOSOUND = False
#NOSOUND = True

from init import *
config = init_config()



root_dir = os.path.dirname(os.path.dirname(__file__))
sound_dir = root_dir + "/sounds"
alphabet_dir = sound_dir + "/alphabet"
alphabet_files = [os.path.join(alphabet_dir, file) for file in os.listdir(alphabet_dir)]





if not NOSOUND:
	import pygame
	pygame.mixer.init()



def playSound(fileName):

	if not NOSOUND:
		sound = pygame.mixer.Sound(fileName)
		playing = sound.play()
		while playing.get_busy():
			pygame.time.delay(10)

def generate_sound(low=3,high=10):
	randomCount = random.randint(low, high)
	files = random.sample(alphabet_files,randomCount)
	word = ""
	for file in files:
		letter = file.split(".")[0].split("/")[-1]
		word += letter
	print("Word is: " + word)
	for file in files:
		playSound(file)

def sound_loop_thread():
	isRunning = False
	loopThread = threading.Thread(target=sound_looper_proc, args=(),name="audio_loop_thread")

	for thread in threading.enumerate():
		if thread.name == "audio_loop_thread":
			isRunning = True
	if isRunning:
		print("audio looper running")
		return 
	else:
		print("starting audio looper")
		loopThread.start()


	


def sound_looper_proc():


	kvs = init_kvs()

	audio_loop_enabled = kvs["audio_loop_enabled"].decode()

	while audio_loop_enabled == "True":
		generate_sound()
		kvs = init_kvs()
		
		audio_loop_interval_low = int(kvs["audio_loop_interval_low"].decode())
		audio_loop_interval_high = int(kvs["audio_loop_interval_high"].decode())

		try:
			sTime = random.randint(audio_loop_interval_low,audio_loop_interval_high)
		except:
			print("Failed to generate random time")
			sTime = ( abs(audio_loop_interval_low) + abs(audio_loop_interval_high) ) / 2

		print("Sleeping for: " + str(sTime) + " seconds")
		time.sleep(sTime)
		audio_loop_enabled = kvs["audio_loop_enabled"].decode()

		
def playSong(fileName):
	if not NOSOUND:
		sound = pygame.mixer.Sound(fileName)
		playing = sound.play()
		while playing.get_busy():
			kvs = init_kvs()
			pygame.time.delay(10)
			audio_song_enabled = kvs["audio_song_enabled"].decode()
			if audio_song_enabled == "False":
				sound.stop()





playSong("/home/pi/gitt/rpid2/sounds/padawan/songs/cantina.wav")



if __name__ == "__main__":



	cc = 5
	c = cc

	while True:


		kvs = init_kvs()
		
	
		audio_loop_enabled = kvs["audio_loop_enabled"].decode()	
		if audio_loop_enabled == "True":
			sound_loop_thread()
		else:
			if c == cc:
				print("audio loop not running")
				c = 0
			else:
				c += 1
	
		time.sleep(3)


