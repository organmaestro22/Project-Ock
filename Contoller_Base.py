from machine import Pin, ADC
import utime
import network
import espnow


# Initialize Wi-Fi in station mode
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# Initialize ESP-NOW
e = espnow.ESPNow()
e.active(True)

# Add the peer's MAC address
#D0:EF:76:34:46:60
#10:06:1C:F6:81:74 old controller
peer_mac = b'\xD0\xEF\x76\x34\x46\x60'  # Replace with the receiver's MAC address
try:
    e.add_peer(peer_mac)
except:
    e.del_peer(peer_mac)
    e.add_peer(peer_mac)

led = Pin(2, Pin.OUT)
BUTTON = Pin(32, Pin.IN)

def constrain(value, min1, max1):
    return max(min(value, max1), min1)

def normalize(value, min1, max1, min2, max2):
    return int(((constrain(value, min1, max1) - min1) / (max1 - min1)) * (max2 - min2) + min2)

def format3(x):
    return f"{x:03}"
def send(p, r, p2, r2, h, a, b):
    p = str(int(p))
    r = str(int(r))
    p2 = str(int(p2))
    r2 = str(int(r2))
    h = str(int(h))
    a = str(int(a))
    b = str(int(b))
    p = format3(p)
    p2 = format3(p2)
    r = format3(r)
    r2 = format3(r2)
    h = format3(h)
    a = format3(a)
    b = format3(b)
    s = p + r + p2 + r2 + h + a + b
    #print(p,r,p2,r2,h,a,b)
    e.send(peer_mac, s)

led.on()
p, r, p2, r2, h, a, b = 500, 500, 500, 500, 500, 500, 500
def buttonOn(p, r, p2, r2, h, a, b):
    global hand, Hand
    while button:
        send(p, r, p2, r2, h, a, b)
    while not button:
        send(p, r, p2, r2, h, a, b)
    while button:
        send(p, r, p2, r2, h, a, b)
    
while True:
    if button:
        buttonOn(p, r, p2, r2, h, a, b)
    else:
        send(p, r, p2, r2, h, a, b)