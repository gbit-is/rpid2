
install_packages() {
	sudo apt install hostapd dnsmasq -y
	sudo systemctl disable hostapd --now
	sudo systemctl disable dnsmasq --now
	sudo cp /etc/dnsmasq.conf /etc/dnsmasq.conf_original

}


#install_packages

