# Install rpid2

## Big steps
- Setup a raspberry pi with raspbian
- Solder the micro-controller -> motor-controller boards ..... which I am yet to document
- Get yourself a wireless USB gamepad 

## installing the software


- if you are OK with running stuff directly from curl .....	

``` 
curl  https://github.com/gbit-is/rpid2/blob/main/setup/scripts/init.sh | bash 
cd /opt/rpid2/setup/scripts
./setup_all.sh
``` 


## Config files and parameters

There are 2 config files, rpid2.conf and jdb_init.conf, both in the etc directory

#### rpid2.conf
rpid2.conf, contains static parameters, once that do not change from once the droid is started
The config file provided, is just my live config file
I have tried to keep it commented to explain it, but will be documenting it further

### jdb_init.conf
This is the "Json DataBase initial" config, once the droid is started, it has multiple parameters set, mostly regarding audio settings right now.  
These values change while using the droid, changing the volume parameters, enabling/disabling sound, modifying the speed limiter settings, etc".
This config sets the default values during startup.


