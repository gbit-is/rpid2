#!/usr/bin/env python3

from common import *
import sys

if len(sys.argv) == 1:

	for section in config:
		for field in config[section]:
			value = config[section][field]
			print(section + "|" + field + ":" + value)

elif len(sys.argv) == 2:
	section = sys.argv[1]
	for field in config[section]:
		value = config[section][field]
		print(field + ":" + value)
elif len(sys.argv) == 3:
	section = sys.argv[1]
	field = sys.argv[2]
	value = config[section][field]
	print(value)
