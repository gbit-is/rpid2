<p align="center">
  <img src="https://raw.githubusercontent.com/gbit-is/rpid2/refs/heads/main/http/img/text_logo.svg" alt="banner_logo">
</p>

# What is it ?
RPID2 is a full astromech control system, running of a raspberry pi and some microcontrollers

### Features:
- Compatible with most* USB gamepads and is designed to also work with for example a steamdeck or custom built controllers
- Drive the main motors
- Drive the dome
  - Auto Homing and positioning is still a WIP, it works but I am not happy with how it works
- Automatically generate sounds and manually trigger sounds
- adjust parameters for motor controls, sound and more ** via a web-ui


### WIP:
- Simplify controller to action mapping
- Auto discovery of micro controllers
- automatic integration with [Hyperdome](https://github.com/gbit-is/hyperdome)
- automatic integrtion with [Servo Ducky](https://github.com/gbit-is/Servo-Ducky)


\* I have tried a few off-brand gamepads with usb recievers and they worked, one required some extra hazzle of tricking the OS into thinking it was a diffirent type of controller, but most just worked out of the box  
\*\* more is a WIP

# BOM:
(This BOM is just for the basic features, not for the dome lights or servo controls, which have their own BOM's in their project sites)
- Raspberry Pi * 
- RP2040/RP2350 at least 2 of these (or any other compatible board)
- USB Hub ( simple, unpowered one, the Pi has enough ports but gamepad recievers are large and don't fit with the nested ports
- Sound card, a cheap USB soundcard is enough, it will be playing mp3 files through a speaker inside an astromech, no need to go full audiophile here
- Motor controllers
  - PWM motor controllers for the main leg motors, I am using the mrbaddeley V3 legs, which use brushed DC motors, I am using 2 "cytron md30c" controllers that were fairly priced in my opinion, from what I have seen most brushless motor controllers implement the same dir/pwm or pwm/pwm scheme for controls like most DC motor controllers, so brushless motors should be usable without any code modifications
  - Controller for the dome, it is a much smaller motor, any small PWM motor controller should work here (that works with 3.3V logic and whatever voltage/amperage you plan on putting trough it)
- Wireless USB Gamepad, I am using some cheap knockoff PS4 controller


\* I am using a Raspberry Pi5 (8 GB) but I ran an earlier version of this system off a Raspberry Pi 3 and 4, but that was a simpler version, I will need to do some benchmarking before making any minimal recomendations smaller then a Pi-5-8GB

