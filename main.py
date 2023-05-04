from machine import Pin, PWM, ADC, SoftI2C
from time import sleep
from ssd1306 import SSD1306_I2C
from rotary_irq import RotaryIRQ

out = Pin(27, Pin.OUT)
pwm = PWM(out)
adc_pin = Pin(4)
adc = ADC(adc_pin)
adc.atten(adc.ATTN_11DB)

i2c = SoftI2C( Pin(15), Pin(2),freq=400000)
oled = SSD1306_I2C(128,64, i2c)

sw = Pin(18, Pin.IN, Pin.PULL_UP)
sw = Pin(18, Pin.IN, Pin.PULL_UP)

r= RotaryIRQ(
    pin_num_clk=21, 
    pin_num_dt=19,
    incr=1,
    reverse=True, 
    range_mode=RotaryIRQ.RANGE_UNBOUNDED)

count = 1
freq = 0
b = 1

while True:
    oled.fill(0)

    duty = int((adc.read())/4)
    duty_pct = int((duty * 100)/1024)
    pwm.duty(duty)

    if sw.value() == 0:
        count *= 10
        r.set(value=0)
        freq = b
    if count > 1000 : count = 1

    b = freq + r.value()*count
    if b <= 0: 
        b = 1
        freq = 0

    pwm.freq(b)

    width = int(duty/18)
    width1 = 17+width
    width2 = 71+width

    if width >= 54 or width==0:
        on = 0
    else:
        on = 1

    oled.pixel(0, 0, 1)
    oled.pixel(1, 0, 1)
    oled.pixel(2, 1, 1)
    oled.pixel(1, 2, 1)
    oled.pixel(2, 3, 1)
    oled.pixel(0, 4, 1)
    oled.pixel(1, 4, 1)
    oled.pixel(4, 4, 1)
    oled.pixel(6, 0, 1)
    oled.pixel(7, 0, 1)
    oled.pixel(8, 1, 1)
    oled.pixel(7, 2, 1)
    oled.pixel(8, 3, 1)
    oled.pixel(6, 4, 1)
    oled.pixel(7, 4, 1)
    oled.pixel(11, 2, 1)
    oled.pixel(11, 3, 1)
    oled.pixel(12, 4, 1)
    oled.pixel(13, 2, 1)
    oled.pixel(13, 3, 1)

    oled.hline(16, 3, 5, 1)
    oled.hline(0, 32, 128, 1)
    oled.vline(18, 0, 40,1)

    oled.hline(18, 3, width, 1)
    oled.hline(72, 3, width, 1)

    oled.vline(width1, 4, 1, on)
    oled.vline(width1, 7, 2, on)
    oled.vline(width1, 11, 2, on)
    oled.vline(width1, 15, 2, on)
    oled.vline(width1, 19, 2, on)
    oled.vline(width1, 23, 2, on)
    oled.vline(width1, 27, 2, on)
    oled.vline(width1, 31, 1, on)

    oled.vline(72, 4, 1, on)
    oled.vline(72, 7, 2, on)
    oled.vline(72, 11, 2, on)
    oled.vline(72, 15, 2, on)
    oled.vline(72, 19, 2, on)
    oled.vline(72, 23, 2, on)
    oled.vline(72, 27, 2, on)
    oled.vline(72, 31, 1, on)

    oled.vline(width2, 4, 1, on)
    oled.vline(width2, 7, 2, on)
    oled.vline(width2, 11, 2, on)
    oled.vline(width2, 15, 2, on)
    oled.vline(width2, 19, 2, on)
    oled.vline(width2, 23, 2, on)
    oled.vline(width2, 27, 2, on)
    oled.vline(width2, 31, 1, on)

    oled.text(f"Duty: {duty_pct}%", 0, 41)
    oled.text(f"Freq: {b} Hz", 0, 49)
    oled.text(f"Range: {count}", 0, 57)

    oled.show()

    sleep(0.1)