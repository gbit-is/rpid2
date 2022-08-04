# rpid2
Attention:
The code is very much in the proof of concept stage as is 


# Features 


## Somewhat ready

- Use *any* usb controller (I am using a cheap Trust GXT545)
- Run H-Bridge motor controllers and steer by providing diffirent PWM signals to each wheel 
- randomly generated R2D2 sounds ( [based on this](https://github.com/hug33k/PyTalk-R2D2) )
- Trigger a self-blocking task (press a button on the controller, start a task, will run until it finished, can't retrigger the task until it finishes)
- Trigger a non-blocking task (press a button on the controller, launch a task, can be retriggered regardless of if it has finished or not)
- Trigger a toggleable task (press a button on the controller, launch a task, will run until it finished (if it ever does) or until the button if pressed again)

## Next up

Servo controls 
I have started testing a 16 channel I2C servo controller hat with promising results, I am however yet to recieve my shipment of servo motors (had a couple laying around to test with) and will start working on that once I have servos to work with

Actual uses for the buttons
I decided to start with reading a bit on threading in python and get some basic triggerable actions going before deciding what to use the buttons for 

# Hardware

- A raspberry pi (using a 3B+ for testing, it was the first I grabbed from my electronics box)
- Any game controller (I think so at least, I am using the Trust GXT545 since I could get it cheaply and it uses a USB dongle rather then bluetooth pairing)
- I am using [This shield](https://thepihut.com/products/gpio-screw-terminal-hat) to expand the reach of the GPIO's
- I am using [this shield](https://thepihut.com/products/16-channel-servo-driver-hat-for-raspberry-pi-12-bit-i2c) to control the Servos 
- 12v speakers from the trash I hooked up to the headphone jack of the pi 


# Rough mockup of logic flow

![image](https://user-images.githubusercontent.com/34913299/182890060-4bfeab03-816e-4f9b-a3da-a6fc3891931c.png)
