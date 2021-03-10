# https://www.settorezero.com
# Raspberry Pi Pico - esempio PWM, due uscite con fase invertita
# Regola Duty PWM con un trimmer sul pin 34 (GP28 = ADC2)
# Utilizzato Slice 0, uscita PWM A su pin 21 (GP16)
# e uscita PWM B on fase invertita su pin 22 (GP17)
from machine import Pin, PWM, I2C, ADC
from utime import sleep

PWM_BASE=0x40050000 # this correspond to the first PWM register that is CH0_SR, datasheet p.542

pwmA=PWM(Pin(16)) # GP16
pwmB=PWM(Pin(17)) # GP17
pwmA.freq(150000) # 150kHz
pwmA.duty_u16(int(65535/2)) # duty 50%
pwmB.duty_u16(int(65535/2)) # duty 50%

r=machine.mem32[PWM_BASE] # read the actual CH0_SR register value
machine.mem32[PWM_BASE]=r^(1<<3) # set bit 3
r=machine.mem32[PWM_BASE] # re-read register

trimmerA=ADC(Pin(28)) #GP28, pin 34
medie=500
trimreadA=0
i=0

while True:
    trimreadA+=trimmerA.read_u16()
    i+=1
    if (i==medie):
        trimreadA/=medie
        trimreadA=int(trimreadA)
                
        # riporto il valore medio del trimmer a percentuale
        percentA=int((trimreadA/65000)*100)
        if (percentA>100):
            percentA=100
        
        # riporto la percentuale come valore a 16bit da assegnare al duty cycle
        dutyA=(65535*percentA)/100
        pwmA.duty_u16(int(dutyA))
        pwmB.duty_u16(int(dutyA))
        
        # azzero le variabili usate per fare la media
        i=0
        trimreadA=0
        sleep(0.1)