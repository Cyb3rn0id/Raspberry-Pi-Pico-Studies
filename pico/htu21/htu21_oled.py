from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
import framebuf
from htu21 import HTU21
import utime

i2c = I2C(0,sda=Pin(0),scl=Pin(1),freq=400000)
#sensor = HTU21(i2c, 0x40)
oled = SSD1306_I2C(128, 32, i2c)

# Add some text
oled.text("Raspberry Pi",5,5)
oled.text("Pico",5,15)
oled.show()
'''
while True:
    h = sensor.humidity
    t = sensor.temperature
    print('Hum: {:.2f}%'.format(h))
    print('Tem: {:.2f}°'.format(t))
    utime.sleep(1)
'''