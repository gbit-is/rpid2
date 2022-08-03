import sys
import os
import time
import threading
from sounds import *

rootDir = os.path.dirname(os.path.dirname(__file__))
libDir = rootDir + "/lib"
sys.path.append(libDir)


ykey_stop = False

def akey_pressed():
	t1 = threading.Thread(target=akey_pressed_thread, args=(),name="akey_thread")

	isRunning = False

	for thread in threading.enumerate():
		if thread.name == "akey_thread":
			isRunning = True

	if not isRunning:
		t1.start()
	else:
		print("A key thread already exists")


def akey_pressed_thread():
	print("A key is pressed, sleeping")
	time.sleep(3)
	print("sleep is done for A key")





def bkey_pressed():
	t1 = threading.Thread(target=bkey_pressed_thread, args=())
	t1.start()

def bkey_pressed_thread():
	print("B key pressed: Thread	" + threading.currentThread().getName())
	time.sleep(3)
	print("sleep is done for B key: Thred	" + threading.currentThread().getName())

	
def ykey_pressed():

	global ykey_stop

	t1 = threading.Thread(target=ykey_pressed_thread, args=(),name="ykey_thread")

	isRunning = False

	for thread in threading.enumerate():
		if thread.name == "ykey_thread":
			ykey_stop = True
			isRunning = True

	if not isRunning:
		ykey_stop = False
		t1.start()
	else:
		print("Y key thread existed,variable reset")




def ykey_pressed_thread():
	global ykey_stop
	while not ykey_stop:
		print("yKey")
		time.sleep(0.5)

def xkey_pressed():
        t1 = threading.Thread(target=xkey_pressed_thread, args=(),name="xkey_thread")

        isRunning = False

        for thread in threading.enumerate():
                if thread.name == "xkey_thread":
                        isRunning = True

        if not isRunning:
                t1.start()
        else:
                print("X key thread already exists")


def xkey_pressed_thread():
	randomSound(7,20)















