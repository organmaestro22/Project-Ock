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
e.config(timeout_ms = 250)
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
led = Pin(2, Pin.OUT)

def decodeMSG(msg): # convert a message into its 3 values
    try:
        p = int(msg[0:3])
        r = int(msg[3:6])
        p2 = int(msg[6:9])
        r2 = int(msg[9:12])
        h = int(msg[12:15])
        return [p, r, p2, r2, h]
        
    except:
        print("error")
        return [500, 500, 500, 500, 500]
    
def getCommand(): # wait for the controller to give a command
    while True:
        try:
            host, msg = e.recv()
            if msg:
                led.on()
                return msg
            else:
                led.off()
                PLATFORM.moveTo(0, 0, 0)
                PLATFORM2.moveTo(0, 0, 0)
        except:
            led.off()
            PLATFORM.moveTo(0, 0, 0)
            PLATFORM2.moveTo(0, 0, 0)
            
            
def getPos():
    p, r, p2, r2, h = decodeMSG(getCommand())
    p = p * 130/999 - 65
    r = r * 130/999 - 65
    p2 = p2 * 130/999 - 65
    r2 = r2 * 130/999 - 65
    h = h * 2/999
    return [p, r, p2, r2, h]

A_MOT = Servo(4) # SERVOS
B_MOT = Servo(16)
C_MOT = Servo(17)
D_MOT = Servo(18)
E_MOT = Servo(19)
F_MOT = Servo(21)

PLATFORM = JenningsPlatform(A_MOT, B_MOT, C_MOT, 50, 145, 50, 145, 50, 145, 1) # PLATFROM WITH KINEMATICS
PLATFORM2 = JenningsPlatform(D_MOT, E_MOT, F_MOT, 50, 190, 50, 190, 50, 190, 1) # PLATFROM WITH KINEMATICS
PLATFORM.moveTo(0, 0, 0)
PLATFORM2.moveTo(0, 0, 0)

while True:
    p, r, p2, r2, h = getPos()
    PLATFORM.moveTo(-p, -r, h)
    PLATFORM2.moveTo(p2, -r2, h) # Pitch and roll are negative because platform 2 is rotated 180 degrees
    utime.sleep(.05)

