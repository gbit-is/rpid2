#!/usr/bin/env bash

start_order="apache2 zeodb _bootstrap nanomq rpid2_motor_server rpid2_api_server rpid2_audio_server rpid2_gamepad_reciever"

if [[ "$(whoami)" != "root" ]];then
	echo "script must be run as root"
	exit 1
fi

function init_script(){
	cd /opt/rpid2/bin
	source ../venv/bin/activate
}

function run_hotspot() {
	/opt/rpid2/bin/hotspot/hotspot.sh
}

function fix_soundcard() {

	./list_configs.py sound_card run_sound_card_fixer | grep -i "True" > /dev/null
	if [ $? -eq 0 ];then
		./sound_card_fixer.sh
	fi
}

function start_service() {
	service_name=$1
	first_attemp=$2

	echo "Starting service: $service_name"
	systemctl start $service_name
	sleep 1
	service_status=$(systemctl is-active $service_name)
	if [ $? -ne 0 ];then
		echo "service $service_name did not start correctly"	
		echo "status is: $service_status"
		echo "log entries are:"
		journalctl -u $service_name -since "10seconds ago"

		if [[ "$first_attemp" == "True" ]];then
			echo "Retrying service"
			sleep 1 
			start_service $service_name "False"
		else
			echo "Not retrying to start the service"
		fi

	fi
}

function run_other () {
	name=$1

	if [[ "$name" == "_bootstrap" ]];then
		echo "Running JDB bootstrapper"
		./bootstrap.py

	else
		echo "run_other name $name is not known"
	fi


}

function start_all_services() {
	for item in $start_order;do

		echo $item | grep "^_" > /dev/null
		if [ $? -ne 0 ];then
			start_service $item "True"
			:
		else
			run_other $item
		fi
	


	done
}

init_script
run_hotspot
fix_soundcard
start_all_services


# re-start the motor reciever because of some stupid bug I havent debugged yet
systemctl restart rpid2_motor_server.service

