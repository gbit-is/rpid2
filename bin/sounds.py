import os
import random
import time


NOSOUND = False
#NOSOUND = True


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



def soundGen():
	while True:
		print("make sound")
		randomSound()
		sTime = random.randint(5,18)
		print("Sleeping for: " + str(sTime) + " seconds")
		time.sleep(sTime)
		

if __name__ == "__main__":
	soundGen()
