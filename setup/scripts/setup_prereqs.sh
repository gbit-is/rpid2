#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR
source init.sh


setup_basics() {


	apt install python3 -y 
	apt install python3-venv -y
	apt install apache2 -y



}

setup_nanomq() {

	which nanomq > /dev/null
	if [ $? -eq 0 ];then
		echo "nanomq already installed"
	else
		echo "installing nanomq"
		curl -s https://assets.emqx.com/scripts/install-nanomq-deb.sh | sudo bash
		sudo apt-get install nanomq
		echo "install done"
	fi

	echo "placing nanomq config file"
	sudo cp $base_dir/setup/config_files/nanomq.conf /etc/nanomq.conf
	sudo chown $run_user:$run_group /etc/nanomq.conf

	echo "placing nanomq service file"
	sudo cp $base_dir/setup/service_files/nanomq.service /etc/systemd/system/nanomq.service
	sudo systemctl enable nanomq --now


}

setup_venv() {
	if [ -d $base_dir/venv ];then
		echo "venv already exists"
	else
		echo "setting up venv"
		python3 -m venv $base_dir/venv
	fi

	source $base_dir/venv/bin/activate
}

setup_zeodb() {
	sudo cp $base_dir/setup/service_files/zeodb.service /etc/systemd/system/zeodb.service
	sudo systemctl enable zeodb --now

}

setup_rpid2_services() {

	# Init zeodb, runs once on boot
	sudo cp $base_dir/setup/service_files/zeodb_init.service /etc/systemd/system/zeodb_init.service
	#sudo systemctl enable zeodb_init --now


	# setup the audio management server
	sudo cp $base_dir/setup/service_files/rpid2_audio_server.service /etc/systemd/system/rpid2_audio_server.service
	#sudo systemctl enable rpid2_audio_server --now

	# run the fastapi process
	sudo cp $base_dir/setup/service_files/rpid2_api_server.service /etc/systemd/system/rpid2_api_server.service
	sudo systemctl enable rpid2_api_server --now

}


setup_apache() {

	# Disable any running sites
	a2query -s  2>&1  | grep -v "No site matches" | grep . > /dev/null
	if  [ $? -ne 0 ];then
      		awk '{print $1}' | xargs a2dissite
	fi

	sudo cp $base_dir/setup/config_files/rpid2.conf /etc/apache2/sites-available
	sudo a2ensite rpid2
	sudo systemctl restart apache2
	sudo systemctl enable apache2

	sudo cp -a $base_dir/http/* /var/www/html
	sudo chown -R www-data:www-data /var/www/html

	





}


#setup_venv
#setup_nanomq
#setup_zeodb
#setup_rpid2_services
setup_apache
