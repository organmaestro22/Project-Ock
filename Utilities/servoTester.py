from machine import Pin, ADC, PWM
import utime
import math

led = Pin(2, Pin.OUT)
pwr = Pin(25, Pin.OUT)
pwr.on()

R = ADC(Pin(34)) # CONTROLL STICKS/POTS
P = ADC(Pin(35))

R.atten(ADC.ATTN_11DB) # attenuation for 3.3V
P.atten(ADC.ATTN_11DB)

class Servo:
    def __init__(self,pin_id,min_us=544.0,max_us=2400.0,min_deg=0.0,max_deg=180,freq=50):
        self.pwm = PWM(Pin(pin_id))
        self.pwm.freq(freq)
        self.current_us = 0.0
        self._slope = (min_us-max_us)/(math.radians(min_deg)-math.radians(max_deg))
        self._offset = min_us
        
    def write(self,deg):
        self.write_rad(math.radians(deg))
        
    def write_rad(self,rad):
        self.write_us(rad*self._slope+self._offset)

    def write_us(self,us):
        self.current_us=us
        self.pwm.duty_ns(int(self.current_us*1000.0))

S1 = Servo(12)
S2 = Servo(13)
a = 1
led.on()
while True:
    print(R.read_u16()*90/65535)
    if a:
        S1.write(P.read_u16()*90/65535+R.read_u16()*90/65535)
        S2.write(90+R.read_u16()*90/65535-P.read_u16()*90/65535)
    else:
        S1.write(P.read_u16()*180/65535)
        S2.write(R.read_u16()*180/65535)
    utime.sleep(.05)
