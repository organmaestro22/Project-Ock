from machine import Pin, ADC
import utime
pwr = Pin(13, Pin.OUT)
pwr.on()
pin1 = ADC(Pin(36, Pin.IN)) # middle
pin1.atten(ADC.ATTN_11DB)
pin2 = ADC(Pin(39, Pin.IN)) # index
pin2.atten(ADC.ATTN_11DB)
pin3 = ADC(Pin(34, Pin.IN)) # thumb
pin3.atten(ADC.ATTN_11DB)
pin1vals = []
pin2vals = []
pin3vals = []

while True:
    pin1vals.append(pin1.read_u16())
    pin2vals.append(pin2.read_u16())
    pin3vals.append(pin3.read_u16())
    print(pin3.read_u16())
    utime.sleep(0.1)
    try:
        print(f"1: Max: {max(pin1vals)}, Min: {min(pin1vals)}, 2: Max: {max(pin2vals)}, Min: {min(pin2vals)}, 3: Max: {max(pin3vals)}, Min: {min(pin3vals)}")
    except:
        print(pin3vals)