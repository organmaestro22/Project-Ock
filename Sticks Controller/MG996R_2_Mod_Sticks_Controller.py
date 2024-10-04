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
peer_mac = b'\xD0\xEF\x76\x34\x46\x60'  # Replace with the receiver's MAC address
e.add_peer(peer_mac)

led = Pin(2, Pin.OUT)
pwr = Pin(25, Pin.OUT)
pwr.on()
R = ADC(Pin(34)) # CONTROLL STICKS
P = ADC(Pin(35))
P2 = ADC(Pin(32))
R2 = ADC(Pin(33))
R.atten(ADC.ATTN_11DB) # attenuation for 3.3V
P.atten(ADC.ATTN_11DB)
P2.atten(ADC.ATTN_11DB)
R2.atten(ADC.ATTN_11DB)

# Calibration
R_OFFSET = -R.read_u16() * 999/65535
P_OFFSET = -P.read_u16() * 999/65535
P2_OFFSET = -P2.read_u16() * 999/65535
R2_OFFSET = -R2.read_u16() * 999/65535
BUTTON = Pin(27, Pin.IN, Pin.PULL_DOWN) # CONTROLL STICK BUTTON

def send(p, r, p2, r2, b):
    if p > 999: p = 999
    if r > 999: r = 999
    if p2 > 999: p2 = 999
    if r2 > 999: r2 = 999
    if p < 0: p = 0
    if r < 0: r = 0
    if p2 < 0: p2 = 0
    if r2 < 0: r2 = 0
    p = str(int(p))
    r = str(int(r))
    p2 = str(int(p2))
    r2 = str(int(r2))
    b = str(int((b + 1) * 500 - 1)) 
    p = "00" + p if len(p) == 1 else "0" + p if len(p) == 2 else p
    p2 = "00" + p2 if len(p2) == 1 else "0" + p2 if len(p2) == 2 else p2
    r = "00" + r if len(r) == 1 else "0" + r if len(r) == 2 else r
    r2 = "00" + r2 if len(r2) == 1 else "0" + r2 if len(r2) == 2 else r2
    s = p + r + p2 + r2 + b
    e.send(peer_mac, s)

led.on()
old_p = 500
old_r = 500
old_p2 = 500
old_r2 = 500
WEIGHT = 5
while True:
    p, r, p2, r2 = P.read_u16() * 999/65535 + P_OFFSET + 500, -R.read_u16() * 999/65535 - R_OFFSET + 500, - P2.read_u16() * 999/65535 - P2_OFFSET + 500, - R2.read_u16() * 999/65535 - R2_OFFSET + 500
    p = (p + WEIGHT * old_p)/(WEIGHT + 1)
    p2 = (p2 + WEIGHT * old_p2)/(WEIGHT + 1)
    r = (r + WEIGHT * old_r)/(WEIGHT + 1)
    r2 = (r2 + WEIGHT * old_r2)/(WEIGHT + 1)
    send(p, r, p2, r2, BUTTON.value())
    old_p = p
    old_r = r
    old_p2 = p2
    old_r2 = r2
    utime.sleep(.05)
