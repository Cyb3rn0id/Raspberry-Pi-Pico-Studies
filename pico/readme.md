Every example can contain a `lib` and/or an `img` folder: those folders must be copied in the root of your raspberry pi pico. Then you must copy the .py file of the example in the root too.

In your scripts is not necessary include the libraries by adding _lib/_ : the MicroPython interpreter will look in the _lib_ folder by default.

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

## Notes
Folder structure generated with [ASCII Treewiev generator](https://konohiroaki.github.io/ascii-treeview-generator/)
