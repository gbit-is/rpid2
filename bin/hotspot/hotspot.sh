#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

if [[ "$(whoami)" != "root" ]];then
	echo "script must be run as root"
	exit 1
fi

# eligable interfaces for being connected

cd ..
source ../venv/bin/activate



interfaces="eth0 wlan0"
interfaces=$(./list_configs.py  network_config interfaces)
interfaces=$(echo "$interfaces" | sed 's/,/ /g')
echo "$interfaces"
states=""

# for each eligable interface
for interface in $interfaces;do
	# check the state of the interface, add to "states"
	state=$(ip -json addr show $interface | jq '.[].operstate' -r)
	states="${states}${state}\n"
done

#clean up list due to dirty way of generating said list
states=$(echo -e "$states" | grep .)

# check if any eligable interface is up
echo "$states" | grep "UP" > /dev/null
if [ $? -eq 0 ];then
	echo "a network interface is up"
	echo "no need to continue"
	#exit 0
else
	echo "no network interface is up"
fi


cd $SCRIPT_DIR

./edit_hotspot.sh


echo "stopping onboard WIFI and starting hotspot"

sudo nmcli radio wifi off
sudo pkill -x wpa_supplicant || true
sleep 1
sudo pkill -9 -x wpa_supplicant || true
sudo ip link set wlan0 down
sudo ip addr flush dev wlan0
sudo ip link set wlan0 up
sudo ip addr add 192.168.4.1/24 dev wlan0
sudo systemctl start dnsmasq
sudo systemctl start hostapd

