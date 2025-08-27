#!/usr/bin/env bash

if [[ "$(whoami)" != "root" ]];then
	echo "script must be run as root"
	exit 1
fi

cd /opt/rpid2/bin
source ../venv/bin/activate

services=$(./list_configs.py  services)

for service in $services;do
	service_name=$(echo $service | awk -F ':' '{print $1}')

	systemctl stop $service_name
done
