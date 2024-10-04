from machine import Pin
import utime
led = Pin(2, Pin.OUT)
while True:
    led.on()
    utime.sleep(1)
    led.off()
    utime.sleep(1)