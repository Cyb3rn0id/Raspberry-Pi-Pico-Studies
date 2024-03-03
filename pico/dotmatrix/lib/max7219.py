"""
MicroPython max7219 cascadable 8x8 LED matrix driver
with some minor edits by CyB3rn0id, read the code for single edits

Original library by Mike Causer:
https://github.com/mcauser/micropython-max7219

MIT License
Copyright (c) 2017 Mike Causer
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# (edit by @CyB3rn0id): usage example rewritten and posted here 
"""
Driver for cascading MAX7219 8x8 LED matrices.
Usage example:
>>> from max7219 import Matrix8x8
>>> from machine import Pin, SPI
>>> spi = SPI(0)
>>> cs=Pin(x)
>>> matrixNumber=4
>>> display = max7219.Matrix8x8(spi, cs , matrixNumber)
>>> display.text('1234',0,0,1)
>>> display.show()
"""
        
from micropython import const
import framebuf
from utime import sleep

_NOOP = const(0)
_DIGIT0 = const(1)
_DECODEMODE = const(9)
_INTENSITY = const(10)
_SCANLIMIT = const(11)
_SHUTDOWN = const(12)
_DISPLAYTEST = const(15)

class Matrix8x8:
    def __init__(self, spi, cs, num):
        self.spi = spi
        self.cs = cs
        self.cs.init(cs.OUT, True)
        self.buffer = bytearray(8 * num)
        self.num = num
        fb = framebuf.FrameBuffer(self.buffer, 8 * num, 8, framebuf.MONO_HLSB)
        self.framebuf = fb
        # Provide methods for accessing FrameBuffer graphics primitives. This is a workround
        # because inheritance from a native class is currently unsupported.
        # http://docs.micropython.org/en/latest/pyboard/library/framebuf.html
        # (edit by @CyB3rn0id): I've write "color" instead of col, since "col" confuse me about "column"
        self.fill = fb.fill  # (color=1)
        self.pixel = fb.pixel # (x, y, color=1)
        self.hline = fb.hline  # (x, y, w, color=1)
        self.vline = fb.vline  # (x, y, h, color=1)
        self.line = fb.line  # (x1, y1, x2, y2, color=1)
        self.rect = fb.rect  # (x, y, w, h, color=1)
        self.fill_rect = fb.fill_rect  # (x, y, w, h, color=1)
        self.text = fb.text  # (string, x, y, color=1)
        self.scroll = fb.scroll  # (dx, dy)
        self.blit = fb.blit  # (fbuf, x, y[, key])
        self.init()

    def _write(self, command, data):
        self.cs(0)
        for m in range(self.num):
            self.spi.write(bytearray([command, data]))
        self.cs(1)

    def init(self):
        for command, data in (
            (_SHUTDOWN, 0),
            (_DISPLAYTEST, 0),
            (_SCANLIMIT, 7),
            (_DECODEMODE, 0),
            (_SHUTDOWN, 1),
        ):
            self._write(command, data)
    
    def brightness(self, value):
        if not 0 <= value <= 15:
            raise ValueError("Brightness out of range")
        self._write(_INTENSITY, value)

    def show(self):
        for y in range(8):
            self.cs(0)
            for m in range(self.num):
                self.spi.write(bytearray([_DIGIT0 + y, self.buffer[(y * self.num) + m]]))
            self.cs(1)
    
    # (edit by @CyB3rn0id)
    # this function was added from an example of Fidelius Falcon showed here:
    # https://github.com/FideliusFalcon/rpi_pico_max7219/
    # that was inspired by Alan Wang on Instructables:
    # https://www.hackster.io/alankrantas/simple-covid-19-cases-live-update-display-micropython-4607f2
    # I've only added color parameter to the function of Fidelius Falcon
    # and done minor changes to include it in the Mike Causer library
    def text_scroll(self, text, scroll_delay=0.03, color=1):
        y=0 # better write using y=0 or some long lower case letters are not showed properly
        for x in range(self.num * 8, len(text) * -8 - 1, -1):
            self.fill(not color)
            self.text(text, x, y, color)
            self.show()
            sleep(scroll_delay)