#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR
source init.sh

sudo cp $base_dir/setup/config_files/rpid2.conf /etc/apache2/sites-available
