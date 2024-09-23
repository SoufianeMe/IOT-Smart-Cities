from machine import ADC,Pin,PWM
import utime

LED_PWM = PWM(Pin(18))
ROTARY_ANGLE_SENSOR = ADC(0)
LED_PWM.freq(500)
val = 0

while val<65535:
    val = val+50
    utime.sleep_ms(1)
    LED_PWM.duty_u16(val)
while val>0:
    val = val -50
    utime.sleep_ms(1)
    LED_PWM.duty_u16(val)
