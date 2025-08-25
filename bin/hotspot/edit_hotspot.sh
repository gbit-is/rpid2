#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
NIFS=$'\n'
OIFS=$IFS

cd $SCRIPT_DIR
cd ..
source ../venv/bin/activate

config_file="/etc/hostapd/hostapd.conf"
configs="^wpa_passphrase,wpa_passphrase\n^ssid,ssid\ncountry_code,country_code"
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


raspi_wifi_country=$(raspi-config nonint get_wifi_country)
expected_country=$(./list_configs.py network_config country_code)

if [[ "$raspi_wifi_country" != "$expected_country" ]];then
	echo "Fixing raspi-config country setting"
	raspi-config nonint do_wifi_country $expected_country
else
	echo "raspi-config country setting is correct"
fi


