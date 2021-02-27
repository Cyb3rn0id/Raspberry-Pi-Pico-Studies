# https://www.settorezero.com
# Raspberry Pi Pico - esempio PWM
# PWM 150kHz, duty 50%

from machine import Pin, PWM

pwm=PWM(Pin(16)) # GP16
pwm.freq(150000) # 150kHz
pwm.duty_u16(int(65535/2)) # duty 50%

# on the oscillosocope I found this behaviour:
# pwm.freq    Oscilloscope reading
# 149000      148998
# 149100      154107
# 149200      148998
# 149300      154107
# 149400      154107
# 149500      154107
# 149600      150705
# 149700      156006
# 149800      151236
# 149900      154107
# 150000      154107