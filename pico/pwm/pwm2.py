# https://www.settorezero.com
# Raspberry Pi Pico - esempio PWM
# Regola Duty PWM con un trimmer sul pin 34 (GP28 = ADC2)
# Utilizzato Slice 0, uscita PWM su pin 21 (GP16)
# e uscita PWM su pin 22 (GP17)
# i duty vengono regolati in maniera opposta
# Utilizzato un display Oled 128x32 su I2C (GP9=SCL, GP8=SDA)

from machine import Pin, PWM, I2C, ADC
from ssd1306 import SSD1306_I2C
import framebuf
from utime import sleep

# set-up display oled
WIDTH=128
HEIGHT=32
i2c=I2C(0) # Inizializza I2C con settaggi default modulo I2C0, SCL=Pin(GP9), SDA=Pin(GP8)
oled=SSD1306_I2C(WIDTH, HEIGHT, i2c)
oled.fill(0)
oled.text("Test PWM",0,0)
oled.text("Duty A: ",0,8)
oled.text("Duty B: ",0,16)
oled.show()

pwmA=PWM(Pin(16)) # GP16
pwmB=PWM(Pin(17)) # GP17
pwmA.freq(150000) # 150kHz
pwmA.duty_u16(0) # duty cycle iniziale a 0 per l'uscita A
pwmB.duty_u16(0) # duty cycle iniziale a 0 per l'uscita B

trimmer=ADC(Pin(28)) #GP28, pin 34
medie=500
trimread=0
i=0

while True:
    trimread+=trimmer.read_u16()
    i+=1
    if (i==medie):
        trimread/=medie
        trimread=int(trimread)
        
        # riporto il valore medio del trimmer a percentuale
        percentA=int((trimread/65000)*100)
        if (percentA>100):
            percentA=100
        
        # percentuale di B
        percentB=100-percentA
        
        # scrivo sul display
        oled.fill_rect(56, 8, 50, 8, 0) # cancello la parte precedente col valore di Duty
        oled.fill_rect(56, 16, 50, 16, 0) # cancello la parte precedente col valore di Duty
        oled.text(str(int(percentA))+"%",56,8)
        oled.text(str(int(percentB))+"%",56,16)
        oled.show()
        
        # riporto la percentuale come valore a 16bit da assegnare al duty cycle
        dutyA=(65535*percentA)/100
        dutyB=(65535*percentB)/100
        pwmA.duty_u16(int(dutyA))
        pwmB.duty_u16(int(dutyB))
        
        # azzero le variabili usate per fare la media
        i=0
        trimread=0
        sleep(0.1)