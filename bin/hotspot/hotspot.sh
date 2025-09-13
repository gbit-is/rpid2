#!/usr/bin/env bash
#set -x


wifi_check_max=10

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

if [[ "$(whoami)" != "root" ]];then
	echo "script must be run as root"
	exit 1
fi


cd ..
source ../venv/bin/activate


rfkill list | grep "Wireless" -A2 | grep "blocked" | grep yes > /dev/null
if [ $? -eq 0 ];then
	echo "wifi is being softblocked, unblocking wifi"
        rfkill unblock wifi
fi

nmcli radio | grep "disabled" > /dev/null
if [ $? -eq 0 ];then
	echo "wifi is disabled in nmcli,enabling it"
	nmcli radio wifi on
fi




has_wifi="False"
try_wifi="False"
wifi_checks=0

while [[ "$try_wifi" == "True" ]];do
	# eligable interfaces for being connected
	interfaces=$(./list_configs.py  network_config interfaces)
	interfaces=$(echo "$interfaces" | sed 's/,/ /g')
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
		try_wifi="False"
		has_wifi="True"
	else
		echo "no network interface is up"
	fi

	wifi_checks=$((wifi_checks + 1))

	if [ $wifi_checks -gt $wifi_check_max ];then
		echo "given up on finding wifi"
		try_wifi="False"
	fi

	sleep 1

done


cd $SCRIPT_DIR

./edit_hotspot.sh




echo "stopping onboard WIFI and starting hotspot"

#sudo nmcli radio wifi off
#sudo pkill -x wpa_supplicant || true
#sleep 1
#sudo pkill -9 -x wpa_supplicant || true
#sudo ip link set wlan0 down
#sudo ip addr flush dev wlan0




rfkill list | grep "Wireless" -A2 | grep "blocked" | grep yes > /dev/null
if [ $? -eq 0 ];then
	rfkill unblock wifi
fi


nmcli radio | grep "disabled" > /dev/null
if [ $? -eq 0 ];then
	echo "wifi is disabled in nmcli,enabling it"
	nmcli radio wifi on
fi

cd ..
WLAN=$(./list_configs.py network_config interface)

echo "$WLAN"
echo "......"
sudo ip link set $WLAN up
sleep 1
sudo ip addr add 192.168.4.1/24 dev $WLAN
sleep 1
sudo systemctl start dnsmasq
sleep 1
sudo systemctl start hostapd
sleep 1



