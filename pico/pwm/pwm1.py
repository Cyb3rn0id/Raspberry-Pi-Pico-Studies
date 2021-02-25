# https://www.settorezero.com
# Raspberry Pi Pico - esempio PWM
# Regola Duty PWM con un trimmer sul pin 34 (GP28 = ADC2)
# Utilizzato Slice 0, uscita PWM su pin 21 (GP16)
# L'altra uscita dello slice 0 (GP17) non è usata e usata come normale GPIO, a livello basso
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
oled.text("Duty: ",0,8)
oled.show()

pwm=PWM(Pin(16)) # GP16
pwm.freq(150000) # 150kHz
pwm.duty_u16(0) # duty cycle iniziale a 0
gpio = Pin(17, Pin.OUT) #GP17 usato come normale I/O
gpio.value(0) # GP17 a livello basso

trimmer=ADC(Pin(28)) #GP28, pin 34
medie=500 # numero di valori letti dal trimmer su cui fare la media
trimread=0
i=0

while True:
    trimread+=trimmer.read_u16()
    i+=1
    if (i==medie):
        trimread/=medie
        trimread=int(trimread)
        
        # riporto il valore medio del trimmer a percentuale
        percent=int((trimread/65000)*100)
        if (percent>100):
            percent=100
        
        # scrivo sul display
        oled.fill_rect(56, 8, 50, 8, 0) # cancello la parte precedente col valore di Duty
        oled.text(str(int(percent))+"%",56,8)
        oled.show()
        
        # riporto la percentuale come valore a 16bit da assegnare al duty cycle
        duty=(65535*percent)/100
        pwm.duty_u16(int(duty))
        
        # azzero le variabili usate per fare la media
        i=0
        trimread=0
        sleep(0.1)