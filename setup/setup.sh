#!/usr/bin/env bash

git_ssh_link="git@github.com:gbit-is/rpid2_.git"
git_http_link="https://github.com/gbit-is/rpid2_.git"
base_dir="/opt/rpid2"
run_user="pi"
run_group="pi"



which git > /dev/null
if [ $? -ne 0 ];then
	echo "Git is not installed, install git before trying again"
	exit
fi


if [[ $(whoami) != "$run_user" ]];then
	echo "should be run as user pi"
	exit
fi


if [ ! -d "$base_dir" ];then
	echo "pulling repo"
	sudo mkdir /opt/rpid2
	sudo chown $run_user:$run_group $base_dir
	git clone $git_ssh_link $base_dir
else
	cd $base_dir
	echo "Pulling latest....."
	git pull
	if [ $? -ne 0 ];then
		echo "Can't pull git repo ... setup wrong or something ?"
		exit 
	fi

fi
