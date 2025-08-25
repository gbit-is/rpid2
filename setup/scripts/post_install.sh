#!/usr/bin/env bash


if [[ "$(whoami)" != "root" ]];then
	echo "script must be run as root"
	exit 1
fi


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR
source init.sh

SERVICE_DIR="$base_dir/setup/service_files"

cd $SERVICE_DIR

sudo cp $base_dir/setup/service_files/rpid2.service /etc/systemd/system/rpid2.service 


systemctl daemon-reload

for service in $(ls $SERVICE_DIR/*service);do
	service_name=$(echo "$service" | awk -F '/' '{print $NF}')
	sudo systemctl disable $service_name
done



systemctl daemon-reload

systemctl enable rpid2 --now
