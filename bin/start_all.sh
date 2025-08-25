#!/usr/bin/env bash


if [[ "$(whoami)" != "root" ]];then
	echo "script must be run as root"
	exit 1
fi



#/opt/rpid2/bin/hotspot/hotspot.sh

# Start ZEODB
systemctl start zeodb

# start apache, if not started
systemctl start apache2

# bootstrap init values for zeodb
cd /opt/rpid2/bin
source ../venv/bin/activate; ./bootstrap.py

# start NanoMQ
systemctl start nanomq

# start the API server
systemctl start rpid2_api_server.service

# Start the motor server
systemctl start rpid2_motor_server.service

# start the audio server
systemctl start rpid2_audio_server.service

# start the gamepad reciever
systemctl start rpid2_gamepad_reciever.service



