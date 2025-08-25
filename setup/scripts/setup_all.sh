#!/usr/bin/env bash



if [[ "$(whoami)" != "root" ]];then
	echo "script must be run as root"
	exit 1
fi


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR



echo "SOURCING CONFIG FILE"
source init.sh


echo "INSTALLING RPID2 MAIN SOFTWARE"
./setup_prereqs.sh

echo "INSATALLING HOTSPOT SOFTWARE"
./setup_hotspot.sh

echo "Running post_install.sh"
./post_install.sh






