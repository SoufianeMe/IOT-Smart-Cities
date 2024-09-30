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
    d.clear()
    d.setCursor(0,0)
    d.print(text1)
    d.setCursor(0,1)
    d.print(text2)
    
def Clignoter():
    global startcli
    if time.ticks_diff(time.ticks_ms(),startcli) > 500 and time.ticks_diff(time.ticks_ms(),startcli) < 600:
        PrintLed("ALARM","")
    if time.ticks_diff(time.ticks_ms(),startcli) > 1000:
        d.clear()
        startcli=time.ticks_ms()
    #if time.ticks_diff(time.ticks_ms(),startcli) > 300:
    #    PrintLed("ALARM","")
    
def Defiler():
    global startcli
    list=["ALARM"," ALARM","  ALARM","   ALARM","    ALARM","     ALARM","      ALARM","       ALARM"]
    if time.ticks_diff(time.ticks_ms(),startcli) > 500 and time.ticks_diff(time.ticks_ms(),startcli) < 600:
        PrintLed(list[0],"")
    if time.ticks_diff(time.ticks_ms(),startcli) > 800 and time.ticks_diff(time.ticks_ms(),startcli) < 1000:
        PrintLed(list[1],"")
    if time.ticks_diff(time.ticks_ms(),startcli) > 1200 and time.ticks_diff(time.ticks_ms(),startcli) < 1400:
        PrintLed(list[2],"")
    if time.ticks_diff(time.ticks_ms(),startcli) > 1600 and time.ticks_diff(time.ticks_ms(),startcli) < 1800:
        PrintLed(list[3],"")
    if time.ticks_diff(time.ticks_ms(),startcli) > 2000 and time.ticks_diff(time.ticks_ms(),startcli) < 2200:
        PrintLed(list[4],"")
        startcli=time.ticks_ms()

        
    
def Afficher(tempset,temp):
    global startlcd
    if time.ticks_diff(time.ticks_ms(),startlcd) > 100:
        PrintLed("Set: "+str(tempset),"Ambient: "+str(temp))
        startlcd = time.ticks_ms()
    
temp,humid = dht.readTempHumid()
tempset = (ROTARY_ANGLE_SENSOR.read_u16()*35/65535)

while True:

    if time.ticks_diff(time.ticks_ms(),start) > 1000:
        start = time.ticks_ms()
        temp,humid = dht.readTempHumid()
        tempset = (ROTARY_ANGLE_SENSOR.read_u16()*35/65535) 
    if temp < (tempset+3) and temp > tempset:
        Afficher(tempset,temp)
        buzzer.duty_u16(0)
        Breathing(500)
    elif temp > (tempset+3):
        buzzer.freq(500)
        buzzer.duty_u16(1000)
        Breathing(2000)
        #Clignoter()
        Defiler()
    else:
        Afficher(tempset,temp)
        buzzer.duty_u16(0)
        Breathing(500)
        
        
        
        
                
        
    
    
    
    
    
