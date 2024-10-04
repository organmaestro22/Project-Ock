import network
import espnow
import time
from machine import Pin

led = Pin(2, Pin.OUT)
# Initialize Wi-Fi in station mode
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Initialize ESP-NOW
e = espnow.ESPNow()
e.active(True)

# Add the sender's MAC address
#FC:E8:C0:74:87:60
peer_mac = b'\xFC\xE8\xC0\x74\x87\x60'  # Replace with the sender's MAC address
e.add_peer(peer_mac)

timeout = time.time() + 60
# Wait for a message
while True:
    host, msg = e.recv()
    print(msg)