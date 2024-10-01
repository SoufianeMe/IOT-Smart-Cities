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
phase = "Montante"

def Breathing(vitesse):
    global val,startled,phase
    if time.ticks_diff(time.ticks_ms(),startled) > 10:
        startled = time.ticks_ms()
        if val <= 0:
            phase = "Montante"
        if val >= 65000:
            phase = "Descendante"
        if phase == "Montante":
            val += vitesse
        if phase == "Descendante":
            val -= vitesse
        LED.duty_u16(val)
        
def PrintLed(text1,text2):
    d.setCursor(0,0)
    d.print(text1)
    d.setCursor(0,1)
    d.print(text2)
    
def Clignoter(tempset):
    global startcli
    elapsed = time.ticks_diff(time.ticks_ms(),startcli)
    if 300 < elapsed < 900:
        PrintLed("ALARM",f"Tempset: {tempset:.2f}")
    if time.ticks_diff(time.ticks_ms(),startcli) > 1000:
        d.clear()
        startcli=time.ticks_ms()

def Defiler(tempset):
    global startcli
    elapsed = time.ticks_diff(time.ticks_ms(),startcli)
    list=["ALARM"," ALARM","  ALARM","   ALARM","    ALARM","     ALARM","      ALARM","       ALARM"]
    index = (elapsed // 300) % len(list)
    if index < len(list):
        PrintLed(list[index],f"Tempset: {tempset:.2f}")
    if elapsed > 2400:
        d.clear()
        startcli = time.ticks_ms()
        
    
def Afficher(tempset,temp):
    global startlcd
    if time.ticks_diff(time.ticks_ms(),startlcd) > 100:
        PrintLed(f"Set: {tempset:.2f}",f"Ambient: {temp:.2f}")
        startlcd = time.ticks_ms()
    
temp,humid = dht.readTempHumid()
tempset = (ROTARY_ANGLE_SENSOR.read_u16()*35/65535)

while True:

    if time.ticks_diff(time.ticks_ms(),start) > 1000:
        start = time.ticks_ms()
        temp,humid = dht.readTempHumid()
        tempset = 15 + (ROTARY_ANGLE_SENSOR.read_u16()*20/65535)
    if temp < (tempset+3) and temp > tempset:
        Afficher(tempset,temp)
        buzzer.duty_u16(0)
        Breathing(500)
    elif temp > (tempset+3):
        buzzer.freq(500)
        buzzer.duty_u16(500)
        Breathing(2000)
        #Clignoter(tempset)
        Defiler(tempset)
    else:
        Afficher(tempset,temp)
        buzzer.duty_u16(0)
        Breathing(500)
        
        
        
        
                
        
    
    
    
    
    
