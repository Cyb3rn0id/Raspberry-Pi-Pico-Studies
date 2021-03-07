`_lib` and `_img` folder must be on the Raspberry Pi Pico without the underscore (I've added it only for showing those 2 folder on top of the list).  

Examples are contained in each folder grouped for theme, but scripts (_*.py_) must be copied on the root of Raspberry Pi Pico, without folders.

Is not necessary include the libraries by adding _lib/_ : the MicroPython interpreter will look in the _lib_ folder by default.

Example of Raspberry Pi Pico folder structure:
```
[root]
├─ img
│   └─ szlogo.pbm
├─ lib
│   ├─ max7219.py
│   ├─ ssd1306.py
│   └─ 
├─ blink_del.py
├─ blink_int.py
├─ dotmatrix.py
├─ neopixel.py
├─ oled_logo.py
├─ oled.py
├─ pwm1.py
├─ pwm2.py
├─ pwm3.py
└─ pwm150khz.py
```