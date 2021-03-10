# https://www.settorezero.com
# Raspberry Pi Pico - esempio PWM
# PWM 150kHz, duty 50%, channel B with phase inverted

from machine import Pin, PWM

PWM_BASE=0x40050000 # this correspond to the first PWM register that is CH0_SR, datasheet p.542

pwmA=PWM(Pin(16)) # GP16
pwmB=PWM(Pin(17)) # GP17
pwmA.freq(150000) # 150kHz
pwmA.duty_u16(int(65535/2)) # duty 50%
pwmB.duty_u16(int(65535/2)) # duty 50%
r=machine.mem32[PWM_BASE] # read the actual CH0_SR register value
print(r) # will print 1 => only EN (bit 0) set 
machine.mem32[PWM_BASE]=r^(1<<3) # set bit 3
r=machine.mem32[PWM_BASE] # re-read register
print(r) #will print 9 => now also the B_INV bit (bit 3) is set