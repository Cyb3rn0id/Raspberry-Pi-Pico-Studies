# Esempio personalizzato logo settorezero
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
from utime import sleep

WIDTH  = 128
HEIGHT = 32

i2c = I2C(0)                                            # Init I2C using I2C0 defaults, SCL=Pin(GP9), SDA=Pin(GP8), freq=400000
print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # Display device address
print("I2C Configuration: "+str(i2c))                   # Display I2C config

oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display

# immagine in formato pbm (32x32) caricata sul Raspberry Pi Pico
# tramite Thonny
with open('img/szlogo.pbm', 'rb') as imgfile:
    for i in range(3):
        imgfile.readline() 
    data = bytearray(imgfile.read()) # file => array

# array => framebuffer
imagebuffer = framebuf.FrameBuffer(data, 32, 32, framebuf.MONO_HLSB)

# pulisce il display
oled.fill(0)

# buffer immagine => framebuffer display oled
oled.blit(imagebuffer, 96, 0)

# aggiungo del testo
oled.text("SETTOREZERO",0,0)
oled.text("Play",0,8)
oled.text("Embedded",0,16)
oled.text("Electronics",0,24)

# framebuffer display => pannello display
oled.show()

# faccio lampeggiare il display
while True:
    sleep(1)
    oled.invert(1)
    sleep(1)
    oled.invert(0)