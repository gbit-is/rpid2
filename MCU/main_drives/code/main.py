import board
import busio
import digitalio
import time
import json
import motors
import usb_cdc





uart = usb_cdc.data

#uart = busio.UART(board.GP16, board.GP17, baudrate=9600)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT



def STOPALL():
    print("RED ALERT")
    right_motor.drive(0)
    left_motor.drive(0)


PWM_FREQ = 20000
LMR = False
RMR = False

# PWM-Pin,Dir-Pin,PWM-Frequency, Reverse-Direction?
left_motor = motors.motor(board.GP14,board.GP15,PWM_FREQ,LMR)
right_motor = motors.motor(board.GP17,board.GP16,PWM_FREQ,RMR)


no_command_count = 0
max_no_command_count = 64

package = b""

while True


    frag = uart.read(1)
    if frag is not None:
        package += frag


    if "@" in package:
        data = package.decode().replace("|","").replace("@","").split(",")
        left = float(data[0])
        right = float(data[1])
        print(left,right)
        no_command_count = 0
        led.value = not led.value
        left_motor.drive(left)
        right_motor.drive(right)
        package = b""

    no_command_count += 1
    if no_command_count > max_no_command_count:
            STOPALL()


