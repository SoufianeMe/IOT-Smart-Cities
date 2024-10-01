from lcd1602 import LCD1602
from dht11 import *
from machine import I2C,Pin,ADC,PWM
from utime import sleep

i2c = I2C(1,scl=Pin(7), sda=Pin(6), freq = 400000)
d = LCD1602(i2c, 2, 16)
d.display()
dht = DHT(18)
buzzer = PWM(Pin(16))

while True: 
    sleep(1)
    temp,humid = dht.readTempHumid()
    d.clear()
    d.setCursor(0,0)
    d.print("Temp:"+str(temp))
    d.setCursor(0,1)
    d.print("Humid: "+str(humid))
    if temp > 30 or humid < 30:
        buzzer.freq(1000)
        buzzer.duty_u16(1000)
    else:
        buzzer.duty_u16(0)