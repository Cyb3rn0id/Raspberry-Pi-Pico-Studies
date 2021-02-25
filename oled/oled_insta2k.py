# animation for 2k followers on instagram
from ssd1306 import SSD1306_I2C
import machine
import time
import uos
import framebuf

WIDTH = 128
HEIGHT = 32

i2c = machine.I2C(0)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
oled.fill(0)

with open('img/insta2k.pbm', 'rb') as imgfile:
    for i in range(3):
        imgfile.readline() 
    data = bytearray(imgfile.read())

img1 = framebuf.FrameBuffer(data, 128, 32, framebuf.MONO_HLSB)
imgfile=None

with open('img/instathank.pbm', 'rb') as imgfile:
    for i in range(3):
        imgfile.readline() 
    data = bytearray(imgfile.read())

img2 = framebuf.FrameBuffer(data, 128, 32, framebuf.MONO_HLSB)
imgfile=None

while True:
    oled.blit(img1, 0, 0)
    oled.show()
    time.sleep(1)
    
    for x in range(4):
        oled.invert(1)
        time.sleep(0.8)
        oled.invert(0)
        time.sleep(0.8)
        
    oled.fill(0)
    oled.blit(img2, 0, 0)
    oled.show()
    time.sleep(3)
    oled.fill(0)   