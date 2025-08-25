#!/usr/bin/env bash



if [[ "$(whoami)" != "root" ]];then
	echo "script must be run as root"
	exit 1
fi


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR
source init.sh
source ${base_dir}/venv/bin/activate



install_packages() {
	sudo apt install hostapd dnsmasq jq -y
	sudo systemctl disable hostapd --now
	sudo systemctl disable dnsmasq --now

}

add_conf_files(){

	## Set the config file for the hostapd daemon
	sudo sed -i '/DAEMON_CONF/d' /etc/default/hostapd
	echo 'DAEMON_CONF="/etc/hostapd/hostapd.conf"' | sudo tee -a  /etc/default/hostapd > /dev/null


	## create a dnsmasq config
	#sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf_original
	sudo cp $base_dir/setup/config_files/dnsmasq.conf /etc/dnsmasq.conf

	sudo cp $base_dir/setup/config_files/dhcpd.conf /etc/dhcpcd.conf

	
	sudo cp $base_dir/setup/config_files/hostapd.conf  /etc/hostapd/hostapd.conf



}

### not set up as a standalone service
#add_service(){
	#sudo cp $base_dir/setup/service_files/rpid2_hotspot.service /etc/systemd/system/rpid2_hotspot.service
#}

install_packages
add_conf_files
#add_service
