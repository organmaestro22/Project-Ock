import network
import espnow
from machine import Pin
import utime

# Initialize Wi-Fi in station mode
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
led = Pin(2, Pin.OUT)
# Initialize ESP-NOW
e = espnow.ESPNow()
e.active(True)

# Add the peer's MAC address
#D0:EF:76:34:46:60
peer_mac = b'\xD0\xEF\x76\x34\x46\x60'  # Replace with the receiver's MAC address
e.add_peer(peer_mac)

# Send a message
for i in range(20):
    led.on()
    e.send(peer_mac, "on")
    utime.sleep(1)
    led.off()
    e.send(peer_mac, "off")
    utime.sleep(1)
    
