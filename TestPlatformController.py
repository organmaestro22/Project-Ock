from machine import Pin, ADC
import utime
import network
import espnow


# Initialize Wi-Fi in station mode
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
led = Pin(2, Pin.OUT)
# Initialize ESP-NOW
e = espnow.ESPNow()
e.active(True)

# Add the peer's MAC address
#D0:EF:76:34:46:60
#10:06:1C:F6:81:74 for platform
peer_mac = b'\x10\x06\x1C\xF6\x81\x74'  # Replace with the receiver's MAC address
e.add_peer(peer_mac)

led = Pin(2, Pin.OUT)
R = ADC(Pin(34)) # CONTROLL STICKS
P = ADC(Pin(35))
Z = ADC(Pin(32))
R.atten(ADC.ATTN_11DB) # attenuation for 3.3V
P.atten(ADC.ATTN_11DB)
Z.atten(ADC.ATTN_11DB)

# Calibration
R_OFFSET = -R.read_u16() * 999/65535
P_OFFSET = -P.read_u16() * 999/65535
Z_OFFSET = -Z.read_u16() * 999/65535
BUTTON = Pin(27, Pin.IN, Pin.PULL_DOWN) # CONTROLL STICK BUTTON

def send(p, r, z):
    if p > 999: p = 999
    if r > 999: r = 999
    if z > 999: z = 999
    if p < 0: p = 0
    if r < 0: r = 0
    if z < 0: z = 0
    p = str(int(p))
    r = str(int(r))
    z = str(int(z))
    p = "00" + p if len(p) == 1 else "0" + p if len(p) == 2 else p
    z = "00" + z if len(z) == 1 else "0" + z if len(z) == 2 else z
    r = "00" + r if len(r) == 1 else "0" + r if len(r) == 2 else r
    s = p + r + z
    e.send(peer_mac, s)

led.on()
while True:
    send(P.read_u16() * 999/65535 + P_OFFSET + 500, -R.read_u16() * 999/65535 - R_OFFSET + 500, - Z.read_u16() * 999/65535 - Z_OFFSET + 500)
    utime.sleep(.05)
    if BUTTON.value() == 1:
        led.off()
        while BUTTON.value() == 1:
            utime.sleep(.05)
        while BUTTON.value() == 0:
            utime.sleep(.05)
        led.on()
        while BUTTON.value() == 1:
            utime.sleep(.05)
