from kinematics import JenningsPlatform
from servo import Servo
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
e.config(timeout_ms = 1000)
# Add the sender's MAC address
#FC:E8:C0:74:87:60 for sticks
#AC:15:18:D8:A0:08 for hand
peer_mac = b'\xAC\x15\x18\xD8\xA0\x08'  # Replace with the sender's MAC address
e.add_peer(peer_mac)

# Uncomment to test recieve
"""while True:
    host, msg = e.recv()
    if msg:
        p = msg[0:3]
        r = msg[3:6]
        z = msg[6:9]
        print(f"p{p} r{r} z{z}")"""

def decodeMSG(msg): # convert a message into its 3 values
    try:
        p = int(msg[0:3])
        r = int(msg[3:6])
        p2 = int(msg[6:9])
        r2 = int(msg[9:12])
        h = int(msg[12:15])
        a = int(msg[15:18])
        b = int(msg[18:21])
        return [p, r, p2, r2, h, a, b]
        
    except:
        print("error")
        return [500, 500, 500, 500, 500, 500, 500]
    
def getCommand(): # wait for the controller to give a command
    while True:
        try:
            host, msg = e.recv()
            if msg:
                return msg
            else:
                BASE.moveTo(0, 0, 0)
                MID.moveTo(0, 0, 0)
                TOP.moveTo(0, 0, 0)
        except:
            BASE.moveTo(0, 0, 0)
            MID.moveTo(0, 0, 0)
            TOP.moveTo(0, 0, 0)
            
            
def getPos():
    p, r, p2, r2, h, a, b = decodeMSG(getCommand())
    p = p * 130/999 - 65
    r = r * 130/999 - 65
    p2 = p2 * 130/999 - 65
    r2 = r2 * 130/999 - 65
    h = h * 2/999
    a = a * 130/999 - 65
    b = b * 130/999 - 65
    return [p, r, p2, r2, h, a, b]

A1 = Servo(15) # SERVOS
B1 = Servo(2)
C1 = Servo(4)
A2 = Servo(16)
B2 = Servo(17)
C2 = Servo(5)
A3 = Servo(18)
B3 = Servo(19)
C3 = Servo(21)

BASE = JenningsPlatform(A1, B1, C1, 50, 145, 50, 145, 50, 145, 1) # MODULES
MID = JenningsPlatform(A2, B2, C2, 50, 145, 50, 145, 50, 145, 1)
TOP = JenningsPlatform(A3, B3, C3, 50, 190, 50, 190, 50, 190, 1)
BASE.moveTo(0, 0, 0)
MID.moveTo(0, 0, 0)
TOP.moveTo(0, 0, 0)

while True:
    p, r, p2, r2, h, a, b = getPos()
    BASE.moveTo(-p/2, -r/2, .5)
    MID.moveTo(p2, -r2, 1)
    TOP.moveTo(-a, b, h)

