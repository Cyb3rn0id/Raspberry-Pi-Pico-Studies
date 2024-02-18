# Esempio utilizzo modulo Reyax RYLR998
# by Giovanni 'Cyb3rn0id' Bernardo
# Collegamenti Reyax RYLR998:
# RX => GP0
# TX => GP1
# VDD => +3.3V NON fornita da Raspberry Pi Pico perchè il modulo richiede più corrente
# Pulsante su GP16 che chiude verso GND
# led verde A(+) su GP17
# led rosso A(+) su GP15
# Il led verde lampeggia di continuo per avvisare che il programma sta girando
# premendo il tasto viene inviato un messaggio "ON" che, ricevuto da un altro Raspberry Pi Pico
# su cui gira lo stesso programma, fa accendere il led rosso.

from debounced_input import DebouncedInput
from machine import Pin,UART, Timer
import time

uart = UART(0) # default uart.init(baudrate=115200, tx=Pin(0), rx=Pin(1), bits=8, parity=None, stop=2)
loraChannel=0
button=16
led = Pin("LED", Pin.OUT) # led integrato su Raspberry Pi Pico/W
ledG = Pin(17, Pin.OUT)
ledR = Pin(15, Pin.OUT)

ledTimer = Timer()

def tick(timer):
    global ledG
    ledG.toggle()

ledTimer.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)

# funzione per inviare messaggi dal modulo
def send_message(channel, msg):
    message='AT+SEND={},{},{}\r\n'.format(channel,len(msg),msg)
    print(message)
    uart.write(message)
    uart.flush() # attende invio dati
    # resta in attesa fino a che non si svuota il buffer di ricezione
    # dato che il modulo risponde con OK
    while(uart.any()==0):
        continue
    
# callback per funzione di debounce pulsante
def button_cb(pin, pressed, duration_ms):
    if (pressed):
        send_message(loraChannel, 'ON')

# aggancio la funzione di debounce al pulsante e alla callback
DebouncedInput(pin_num=button, callback=button_cb, pin_pull=Pin.PULL_UP, pin_logic_pressed=False)

while True:
    # il buffer di ricezione contiene dati
    if uart.any(): 
        # leggo il buffer
        data = uart.read().decode().strip('\r\n')
        print(data) #esempio dato ricevuto: +RCV=0,2,ON,-12,10
        
        if (data.startswith('+RCV=')):
            data=data.strip('+RCV=')
            parts=data.split(',') #[0]=channel [1]=message length [2]=message [3]=RSSI [4]=SNR
                        
            if (parts[2]=='ON'):
                print('OK')
                ledR.toggle()
        else:
            pass
