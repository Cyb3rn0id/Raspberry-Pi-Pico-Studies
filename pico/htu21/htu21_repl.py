# example from Giovanni Bernardo (@cyb3rn0id)
# shows temperature and humidity from an HTU21 on REPL
# SDA => GP0 (pin 1)
# SCL => GP1 (pin 2)
# power for sensor => VSYS (pin 39)
# GND => pins 3, 8, 13, 18, 23, 28, 33, 38
from machine import I2C, Pin
from htu21 import HTU21
import utime

i2c = I2C(0,sda=Pin(0),scl=Pin(1),freq=400000)
sensor = HTU21(i2c, 0x40)

while True:
    h = sensor.humidity
    t = sensor.temperature
    print('Hum: {:.2f}%'.format(h))
    print('Tem: {:.2f}°'.format(t))
    utime.sleep(1)
