# example from Giovanni Bernardo (@cyb3rn0id)
# prints keys from a matrix keypad
# example created with Elecrow Raspberry Pi Pico Advanced Kit:
# https://www.elecrow.com/raspberry-pi-pico-advanced-kit-with-pico-board-32-modules-and-32-detailed-projects-lessons.html
# part of the code derives from that kit lessons (lesson 27 - simple calculator)
# no libraries required
# having keypad matrix in front, there are 8 pins below (R=row C=columnn)
# R1 R2 R3 R4 C1 C2 C3 C4
# connect to pins:
# 17 16 15 14 12 11 10  9
# that corresponds to gpios:
# 13 12 11 10  9  8  7  6

from machine import Pin, Timer
import utime

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

while True:
    r=keypadRead()
    if (r!=-1):
        print(r)      
    
