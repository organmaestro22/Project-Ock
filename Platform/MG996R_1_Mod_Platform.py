from kinematics import Platform
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
#FC:E8:C0:74:87:60
peer_mac = b'\xFC\xE8\xC0\x74\x87\x60'  # Replace with the sender's MAC address
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
        z = int(msg[6:9])
        return [p, r, z]
    except:
        return [500, 500, 500]
    
def getCommand(): # wait for the controller to give a command
    while True:
        host, msg = e.recv()
        if msg:
            led.on()
            return msg
        else:
            led.off()
            PLATFORM.disable()

def getPos():
    p, r, z = decodeMSG(getCommand())
    p = p * 130.984/999 - 65.492
    r = r * 130.984/999 - 65.492
    z = z * 2.125/999
    return p, r, z

A_MOT = Servo(12) # SERVOS
B_MOT = Servo(13)
C_MOT = Servo(14)

PLATFORM = Platform(A_MOT, B_MOT, C_MOT, 60, 190, 60, 190, 60, 190, 1) # PLATFROM WITH KINEMATICS
PLATFORM.moveTo(0, 0, 0)

while True:
    p, r, z = getPos()
    PLATFORM.moveTo(p, r, z)