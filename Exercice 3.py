from lcd1602 import LCD1602
from dht11 import *
from machine import I2C,Pin,ADC,PWM
from utime import sleep
import utime
import time

i2c = I2C(1,scl=Pin(7), sda=Pin(6), freq = 400000)
d = LCD1602(i2c, 2, 16)
d.display()

dht = DHT(18)

buzzer = PWM(Pin(16))

LED = PWM(Pin(20))
LED.freq(500)

ROTARY_ANGLE_SENSOR = ADC(0)

start = time.ticks_ms()
startled = time.ticks_ms()
startlcd = time.ticks_ms()
startcli = time.ticks_ms()

val = 0
def Breathing(vitesse):
    global val,startled,phase
    print(val)
    if time.ticks_diff(time.ticks_ms(),startled) > 10:
        startled = time.ticks_ms()
        if val == 0:
            val = val + vitesse
            phase = "Montante"
        if val >= 65000:
            val = val - vitesse
            phase = "Descendante"
        if phase == "Montante":
            val = val + vitesse
            LED.duty_u16(val)
        if phase == "Descendante":
            val = val - vitesse
            LED.duty_u16(val)
        
def PrintLed(text1,text2):
    global startlcd
    if time.ticks_diff(time.ticks_ms(),startlcd) > 1000:
        startlcd=time.ticks_ms()
        d.clear()
        d.setCursor(0,0)
        d.print(text1)
        d.setCursor(0,1)
        d.print(text2)
    
def Clignoter():
    global startcli
    if time.ticks_diff(time.ticks_ms(),startcli) > 200:
        startcli=time.ticks_ms()
        PrintLed("ALARM","")
    if time.ticks_diff(time.ticks_ms(),startcli) > 200:
        startcli=time.ticks_ms()
        d.clear()
    if time.ticks_diff(time.ticks_ms(),startcli) > 200:
        startcli=time.ticks_ms()
        PrintLed("ALARM","")    

temp,humid = dht.readTempHumid()
tempset = (ROTARY_ANGLE_SENSOR.read_u16()*35/65535)

while True:

    if time.ticks_diff(time.ticks_ms(),start) > 1000:
        start = time.ticks_ms()
        temp,humid = dht.readTempHumid()
        tempset = (ROTARY_ANGLE_SENSOR.read_u16()*35/65535) 
    if temp < (tempset+3) and temp > tempset:
        PrintLed("Set: "+str(tempset),"Ambient: "+str(temp))
        buzzer.duty_u16(0)
        Breathing(500)
    elif temp > (tempset+3):
        buzzer.freq(500)
        buzzer.duty_u16(1000)
        Breathing(2000)
        Clignoter()
    else:
        PrintLed("Set: "+str(tempset),"Ambient: "+str(temp))
        buzzer.duty_u16(0)
        Breathing(500)
        
        
        
        
                
        
    
    
    
    
    
