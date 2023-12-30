Libraries used in the examples. Those libraries must be copied in a _lib_ folder (without underscore) in the Raspberry Pi Pico root.

- max7219.py : 8x8 led matrices attached to MAX7219. Original library by [Mike Causer](https://github.com/mcauser/micropython-max7219).
- ssd1306.py : OLED displays based on the SSD1306 controller. Tested with 128x32 and 128x64 displays on I2C. This library is the one from [Adafruit](https://github.com/adafruit/micropython-adafruit-ssd1306) that was declared deprecated since Adafruit is developing the CircuitPython one
- dht.py : DHTxx humidity and temperature sensors
- htu21.py : HTU21 humidity and temperature sensor
- i2c_lcd.py + lcd_api.py : lcd display with i2c backpack