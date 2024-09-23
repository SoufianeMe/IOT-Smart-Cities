from machine import Pin, PWM, ADC
from time import sleep

buzzer=PWM(Pin(27))
ROTARY_ANGLE_SENSOR = ADC(0)

def Volume():
    vol = ROTARY_ANGLE_SENSOR.read_u16()
    val = (vol/65535.0)*100
    if vol == 0:
        val = 0
    return int(val)

def DO(time):
    buzzer.freq(1046)
    val = Volume()
    buzzer.duty_u16(val*10)
    sleep(time)
def RE(time):
    buzzer.freq(1175)
    val = Volume()
    buzzer.duty_u16(val*10)
    sleep(time)
def MI(time):
    buzzer.freq(1318)
    val = Volume()
    buzzer.duty_u16(val*10)
    sleep(time)
def FA(time):
    buzzer.freq(1397)
    val = Volume()
    buzzer.duty_u16(val*10)
    sleep(time)
def SO(time):
    buzzer.freq(1568)
    val = Volume()
    buzzer.duty_u16(val*10)
    sleep(time)
def LA(time):
    buzzer.freq(1760)
    val = Volume()
    buzzer.duty_u16(val*10)
    sleep(time)
def SI(time):
    buzzer.freq(1967)
    val = Volume()
    buzzer.duty_u16(val*10)
    sleep(time)
def N(time):
    buzzer.duty_u16(0)
    sleep(time)
while True:
    MI(0.6)  # E
    SI(0.3)  # B
    DO(0.3)  # C
    RE(0.6)  # D
    DO(0.3)  # C
    SI(0.3)  # B
    LA(0.6)  # A
    LA(0.3)   # A
    
    DO(0.3)  # C
    MI(0.6)  # E
    RE(0.3)  # D
    DO(0.3)  # C
    SI(0.6)  # B
    DO(0.3)  # C
    RE(0.6)  # D
    MI(0.6)  # E

    DO(0.6)  # C
    LA(0.6)  # A
    LA(0.3)  # A


