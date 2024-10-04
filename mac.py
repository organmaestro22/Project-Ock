import urequests
import network

def mac2Str(mac): 
    return ':'.join([f"{b:02X}" for b in mac])


# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan_mac = wlan.config('mac')
print(mac2Str(wlan_mac))

wlan.active(False)

while wlan.active() == True:
  pass

print('AP Terminated')
#1: AC:15:18:D8:A0:08
#2: AC:15:18:D8:3B:A8
