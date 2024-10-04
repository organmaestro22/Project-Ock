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

def send(p, r, p2, r2, h):
    if p > 999: p = 999
    if r > 999: r = 999
    if p2 > 999: p2 = 999
    if r2 > 999: r2 = 999
    if h > 999: h = 999
    if p < 0: p = 0
    if r < 0: r = 0
    if p2 < 0: p2 = 0
    if r2 < 0: r2 = 0
    if h < 0: h = 0
    p = str(int(p))
    r = str(int(r))
    p2 = str(int(p2))
    r2 = str(int(r2))
    h = str(int(h))
    p = "00" + p if len(p) == 1 else "0" + p if len(p) == 2 else p #add leading 0's
    p2 = "00" + p2 if len(p2) == 1 else "0" + p2 if len(p2) == 2 else p2
    r = "00" + r if len(r) == 1 else "0" + r if len(r) == 2 else r
    r2 = "00" + r2 if len(r2) == 1 else "0" + r2 if len(r2) == 2 else r2
    h = "00" + h if len(h) == 1 else "0" + h if len(h) == 2 else h
    s = p + r + p2 + r2 + h
    e.send(peer_mac, s)

led.on()
p, r, p2, r2, h = 500, 500, 500, 500, 500
while True:
    send(p, r, p2, r2, h)
    if BUTTON.value() == 1:
        led.off()
        while BUTTON.value() == 1:
            utime.sleep(.05)
            send(p, r, p2, r2, h)
        while BUTTON.value() == 0:
            utime.sleep(.05)
            send(p, r, p2, r2, h)
        led.on()
        while BUTTON.value() == 1:
            utime.sleep(.05)
            send(p, r, p2, r2, h)