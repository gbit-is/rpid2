#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $SCRIPT_DIR

config_file="/etc/hostapd/hostapd.conf"
config_file="/Users/gudrun/Documents/GitHub/rpid2/bin/hostapd.conf"

current_line=$(grep "wpa_passphrase" $config_file)
current_pass=$(echo "$current_line" | awk -F '=' '{print $2}')

source ../venv/bin/activate

new_pass=$(./list_configs.py network_config psk)

if [[ "$current_pass" == "$new_pass" ]]; then
	echo "password is already configured"
else
	new_line="wpa_passphrase=$new_pass"
	sed -i "s/$current_line/$new_line/" $config_file

fi
