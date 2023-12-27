# example from Giovanni Bernardo (@cyb3rn0id)
# shows temperature and humidity on an LCD 16x2 (with I2C backpack) read from a DHT11 sensor
# example created with Elecrow Raspberry Pi Pico Advanced Kit:
# https://www.elecrow.com/raspberry-pi-pico-advanced-kit-with-pico-board-32-modules-and-32-detailed-projects-lessons.html
# this is an alternative to lesson 23 - mini weather station
# SDA => GP0 (pin 1)
# SCL => GP1 (pin 2)
# DHT sensor data => GP2 (pin 4)
# power for display and sensor => VSYS (pin 39)
# GND => pins 3, 8, 13, 18, 23, 28, 33, 38
# copy dht.py, i2c_lcd.py, lcd_api.py in the pico \lib folder

from machine import I2C, Pin
from i2c_lcd import I2cLcd 
import dht

sensor = dht.DHT11(Pin(2, Pin.IN, Pin.PULL_UP))

i2c = I2C(0,sda=Pin(0),scl=Pin(1),freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16) #i2c module, address, rows, columns

while True:
    sensor.measure()
    lcd.move_to(0,0)
    lcd.putstr("Temp: {}".format(sensor.temperature())+chr(223))
    lcd.move_to(0,1)
    lcd.putstr("Humi: {}%".format(sensor.humidity()))
