#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
NIFS=$'\n'
OIFS=$IFS

cd $SCRIPT_DIR

config_file="/etc/hostapd/hostapd.conf"


source ../venv/bin/activate

configs="^wpa_passphrase,wpa_passphrase\n^ssid,ssid"
configs=$(echo -e $configs)

IFS=$NIFS
for config in $configs;do
	match=$(echo "$config" | awk -F ',' '{print $1}')
	key=$(echo "$config" | awk -F ',' '{print $2}')

	config_line=$(grep "$match" $config_file)
	old_value=$(echo "$config_line" | awk -F '=' '{print $2}')
	new_value=$(./list_configs.py network_config $key)

	if [[ "$old_value" == "$new_value" ]];then
		echo "$key is set correctly"

	else
		echo "setting new value for $key"
		new_line="${key}=${new_value}"
		sudo sed -i "s/$config_line/$new_line/" $config_file
	fi

done
