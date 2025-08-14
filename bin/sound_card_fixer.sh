#!/usr/bin/env bash

OIFS=$IFS
NIFS=$'\n'


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $SCRIPT_DIR

source ../venv/bin/activate

sound_card_name=$(./list_configs.py sound_card name)

correct_card=$(aplay -l | grep "$sound_card_name" | awk '{print $2}' | sed 's/://g')

current_card=$( cat /etc/asound.conf  | grep card | awk '{print $2}'| tail -1)

if [ $current_card -ne $correct_card ];then
	current_card_lines=$(cat /etc/asound.conf  | grep card)
	new_line="	card $correct_card"
	IFS=$NIFS
	for line in $current_card_lines;do
		sudo sed -i "s/$line/$new_line/" /etc/asound.conf
	done
	
	

fi

#/etc/asound.conf
