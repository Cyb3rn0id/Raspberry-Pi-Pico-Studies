# example from Giovanni Bernardo (@cyb3rn0id)
# blinks the embedded led using a delay
from machine import Pin
from utime import sleep

# "LED" can be used only if you've updated the micropython .uf2 to the latest versions
# and works with both RPi Pico and RPi Pico W
# on Raspberry Pi Pico, LED is pin 25, on Raspberry Pi Pico W LED is not connected to an
# RP2040 physical pin since is connected to the WiFi module
led = Pin("LED", Pin.OUT)

while True:
    led.toggle()
    sleep(0.5)