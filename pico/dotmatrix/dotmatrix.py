# example derived from a work of
# Fidelius Falcon (https://github.com/FideliusFalcon/rpi_pico_max7219/)

'''
Connections:
MAX7219    Pico Name   Pico GPIO   Pico PIN#
VCC        VBUS                    40
GND        GND                     38
CS         SPI0 CSn    GP5         7
CLK        SPI0 SCK    GP6         9
DIN        SPI0 TX     GP7         10
'''

from max7219 import Matrix8x8
from machine import Pin, SPI
from time import sleep

# Matrix parameters: SPI number, CS PIN, number of MAX7219 ICs (=number of 8x8 matrices)
display = Matrix8x8(SPI(0), Pin(5), 4)

# variables used for the demo
txtScroll = "Scrolling Text"
number=1234

while True:
    # write a number
    display.text(str(number),0,0) # text, x, y[, color]
    display.show()
    sleep(2)
    
    # clear display
    display.fill(0)
    display.show()
    
    #scroll a text (scroll does not need the show() method after)
    display.text_scroll(txtScroll) # [, delay, color]
    sleep(1)