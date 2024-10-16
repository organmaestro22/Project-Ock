from machine import Pin
import utime
import network
import espnow
from powerHand import PowerHand

JCS = False # enable or disable Joint Control Scheme (gyro controls all platforms, fingers do offset from gyro (unenable means fingers control upper platforms and gyro just controls lower))

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
led.on()

#calibration
YG_MIN = -60
XG_MIN = -70
YG_MAX = 60
XG_MAX = 70
T_MIN = 25000
T_MAX = 44000
I_MIN = 47000
I_MAX = 56000
M_MIN = 29000
M_MAX = 40000
R_MIN = 26000
R_MAX = 37000
P_MIN = 32000
P_MAX = 47000

Hand = PowerHand(addr = 0x68, thumb = 33, index = 39, middle = 34, ring = 35, pinky = 32, sda = 26, scl =27, vmot = 14,  button = 25)
Hand.hapticFeedback(65535)
utime.sleep(1)
Hand.hapticFeedback(0)
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

def buttonOn(p, r, p2, r2, h, a, b):
    global Hand
    button = Hand.getButton()
    Hand.hapticFeedback(65535)
    while button:
        send(p, r, p2, r2, h, a, b)
        button = Hand.getButton()
    Hand.hapticFeedback(0)
    while not button:
        send(p, r, p2, r2, h, a, b)
        button = Hand.getButton()
    Hand.hapticFeedback(65535)
    while button:
        send(p, r, p2, r2, h, a, b)
        button = Hand.getButton()
    Hand.hapticFeedback(0)
p, r, p2, r2, h, a, b = 500, 500, 500, 500, 500, 500, 500  
weight = 1
while True:
    hand = Hand.read(.05, 100)
    r = (r * weight + normalize(hand['x'], XG_MIN, XG_MAX, 0, 999))/(weight + 1)
    p = (p * weight + normalize(hand['y'], YG_MIN, YG_MAX, 0, 999))/(weight + 1)
    h = (h * weight + normalize(hand['thumb'], T_MIN, T_MAX, 0, 999))/(weight + 1)
    p2 = (p2 * weight + normalize(hand['index'], I_MIN, I_MAX, 0, 999))/(weight + 1)
    r2 = (r2 * weight + normalize(hand['middle'], M_MIN, M_MAX, 0, 999))/(weight + 1)
    a = (a * weight + normalize(hand['ring'], R_MIN, R_MAX, 0, 999))/(weight + 1)
    b = (b * weight + normalize(hand['pinky'], P_MIN, P_MAX, 0, 999))/(weight + 1)
    if hand['button']:
        buttonOn(p, 999-r, 999-p2, r2, 999-h, a, 999-b)
    else:
        send(p, 999-r, 999-p2, r2, 999-h, a, 999-b)