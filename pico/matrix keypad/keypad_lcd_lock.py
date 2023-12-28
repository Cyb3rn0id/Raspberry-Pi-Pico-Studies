# example from Giovanni Bernardo (@cyb3rn0id)
# reads code from a keypad and matches it with a stored password
# if code is right, a green led lights up and "access granted" is showed on display
# if code is wrong, a red led lights up and "access denied" is showed
# everytime you press a key, sound comes out from buzzer
# different sounds are made in case of wrong or success code
# pressed keys are showed as '*', after 16 chars, row is deleted and
# code storing restarts from the key caused the row overflow
# connections:
# having keypad matrix in front, there are 8 pins below (R=row C=columnn)
# R1 R2 R3 R4 C1 C2 C3 C4
# connect to pins:
# 17 16 15 14 12 11 10  9
# that corresponds to gpios:
# 13 12 11 10  9  8  7  6
# LCD connections:
# SDA => GP0 (pin 1)
# SCL => GP1 (pin 2)
# VCC => VSYS (pin 39)
# GND => pins 3, 8, 13, 18, 23, 28, 33, 38
# red led => anode (+) on GPIO16 (pin 21)
# green led => anode (+) on GPIO17 (pin 22)
# buzzer => (+) on GPIO15 (pin 20) (anyway is not correct connect a buzzer directly to a pin)

from machine import Pin, Timer, I2C, PWM
from i2c_lcd import I2cLcd 
import utime

# your code. use max 16 chars since display is 16 columns
passcode="2177"

led_red = Pin(16, machine.Pin.OUT)
led_green = Pin(17, machine.Pin.OUT)
buzzer = PWM(Pin(15))

keyName = [['1','2','3','A'],['4','5','6','B'],['7','8','9','C'],['*','0','#','D']]
keypadRowPins = [13,12,11,10]
keypadColPins = [9,8,7,6]

row = []
col = []
keypadState = []

for i in keypadRowPins:
    row.append(Pin(i,Pin.IN,Pin.PULL_UP))
    keypadState.append([0,0,0,0])

for i in keypadColPins:
    col.append(Pin(i,Pin.OUT))

i2c = I2C(0,sda=Pin(0),scl=Pin(1),freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16) #i2c module, address, rows, columns

def keypadRead():
    global row
    j_ifPressed = -1
    i_ifPressed = -1

    for i in range(0,len(col)):
        col[i].low()
        utime.sleep(0.005)

        for j in range(0,len(row)):
            pressed = not row[j].value()
            if(pressed and (keypadState[j][i] != pressed)):
                keypadState[j][i] = pressed
            elif(not pressed and (keypadState[j][i] != pressed)):
                keypadState[j][i] = pressed
                j_ifPressed = j
                i_ifPressed = i
        col[i].high()

    if(j_ifPressed != -1 and i_ifPressed != -1):
        return keyName[j_ifPressed][i_ifPressed]
    
    else:
        return -1

def start_condition():
    leds_off()
    lcd.clear()
    lcd.putstr("Enter passcode:")
    lcd.move_to(0,1)

def leds_off():
    led_red.low()
    led_green.low()
    
def checkcode(code):
    if (code==passcode):
        return True
    else:
        return False

def passcode_ok():
    led_green.high()
    lcd.clear()
    lcd.putstr("Access Granted")
    tone(1500,500)

def passcode_nok():
    led_red.high()
    lcd.clear()
    lcd.putstr("Access Denied")
    for i in range (3):
        tone(400,80)
        utime.sleep_ms(200)

def tone(freq,ms):
    buzzer.duty_u16(1000)
    buzzer.freq(freq)
    utime.sleep_ms(ms)
    buzzer.duty_u16(0)

def main():
    c=0
    insertedcode=""
    
    while True:
        r=keypadRead()
        
        if (r!=-1): # user pressed a key
            
            tone(1000,30)
            
            if (r=='#'): # user pressed # key => confirm
                
                # check the inserted code
                if (checkcode(insertedcode)):
                    # code is ok: perform lock opening
                    passcode_ok()
                else:
                    # code is not ok: do nothing
                    passcode_nok()
                
                # reset variables to re-start
                c=0
                insertedcode=""
                utime.sleep(0.5)
                leds_off()
                start_condition()
                
            else: # user pressed a key different than #
                
                c=c+1 # increment key counter
                
                if (c<17): # end of display not reached
                    insertedcode = insertedcode + r # store inserted code
                    lcd.move_to(c-1,1)
                    lcd.putstr("*")
                
                else: # end of display reached: store only the last char and reset
                    c=1
                    insertedcode=r
                    start_condition()
                    lcd.putstr("*")
                    
start_condition()
main()
