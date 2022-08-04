
def init_config():

	import configparser
	config = configparser.ConfigParser()
	config.read('../rpid2.conf')
	return config


def init_libs():
	import sys
	import os
	rootDir = os.path.dirname(__file__)
	if "/." in rootDir:
		rootDir = rootDir.replace("/.","")
	libDir = rootDir + "/lib"
	return libDir

