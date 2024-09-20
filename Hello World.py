import machine
import utime
LED = machine.Pin(16,machine.Pin.OUT)
BUTTON = machine.Pin(18,machine.Pin.IN)
val = 0
while True:
    if BUTTON.value() == 1:
        val = val+1
        for i in range(2):
            LED.value(0)
            utime.sleep(0.1)
            LED.value(1)
            utime.sleep(0.1)
        while (val == 1):
            LED.value(0)
            utime.sleep(0.1)
            LED.value(1)
            utime.sleep(0.1)
            if BUTTON.value() == 1:
                val += 1
    if val == 2:
        for i in range(2):
            LED.value(0)
            utime.sleep(0.05)
            LED.value(1)
            utime.sleep(0.05)
        while (val == 2):
            LED.value(0)
            utime.sleep(0.05)
            LED.value(1)
            utime.sleep(0.05)
            if BUTTON.value() == 1:
                val += 1
    if val == 3:
        LED.value(0)
        utime.sleep(1)
        val = 0
        
        