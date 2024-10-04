from machine import Pin, ADC
import utime
import network
import espnow
from MPU6050 import MPU6050
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
YG_MIN = -1000
XG_MIN = -1000
YG_MAX = 1000
XG_MAX = 1000
MPU_ZERO_ZA = -4
T_MIN = 23000
T_MAX = 42000
I_MIN = 42000
I_MAX = 55000
M_MIN = 23000
M_MAX = 37000
R_MIN = 20000
R_MAX = 28000
P_MIN = 44000
P_MAX = 25000

def constrain(value, min1, max1):
    return max(min(value, max1), min1)

def normalize(value, min1, max1, min2, max2):
    return int(((constrain(value, min1, max1) - min1) / (max1 - min1)) * (max2 - min2) + min2)

def format3(p):
    return "00" + p if len(p) == 1 else "0" + p if len(p) == 2 else p #add leading 0's

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
    #print(s)
    e.send(peer_mac, s)

led.on()
p, r, p2, r2, h, a, b = 500, 500, 500, 500, 500, 500, 500
def buttonOn(p, r, p2, r2, h, a, b):
    global hand, Hand
    while hand['button']:
        send(999 - p, 999 - r, p2, r2, 999 - h, a, b)
        hand = Hand.read(.05, 100)
    while not hand['button']:
        send(999 - p, 999 - r, p2, r2, 999 - h, a, b)
        hand = Hand.read(.05, 100)
    while hand['button']:
        send(999 - p, 999 - r, p2, r2, 999 - h, a, b)
        hand = Hand.read(.05, 100)
    
Hand = PowerHand(addr = 0x68, thumb = 33, index = 39, middle = 34, ring = 35, pinky = 32, sda = 26, scl = 27, vmot = 14, mpu_flat_accel = MPU_ZERO_ZA,  button = 25)
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
        buttonOn(p, r, p2, r2, h, a, b)
    else:
        send(999 - p, 999 - r, p2, r2, 999 - h, a, b)