import network
import esp
esp.osdebug(None)
import gc
gc.collect()
ap = network.WLAN(network.AP_IF)
ap.active(False)

while ap.active() == True:
  pass

print('AP Terminated')

