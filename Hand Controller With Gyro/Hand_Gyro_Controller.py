from machine import Pin, ADC
import utime
import network
import espnow
from MPU6050 import MPU6050

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
pwr = Pin(13, Pin.OUT)
pwr.on()
utime.sleep(.5)
BUTTON = Pin(32, Pin.IN)
mpu = MPU6050(scl = 33, sda = 25)
THUMB = ADC(Pin(34)) # CONTROLL STICKS
MIDDLE = ADC(Pin(36))
INDEX = ADC(Pin(39))
SENS = ADC(Pin(35))
THUMB.atten(ADC.ATTN_11DB) # attenuation for 3lk.3V
MIDDLE.atten(ADC.ATTN_11DB)
INDEX.atten(ADC.ATTN_11DB)
SENS.atten(ADC.ATTN_11DB)

# Calibration
SAMPLES = 100 # number of samples to take of sensor reading per command send
M_MIN = 27000
M_MAX = 41000
I_MIN = 37000
I_MAX = 48000
T_MIN = 23000
T_MAX = 40000
T_MID = (T_MIN + T_MAX) / 2
M_MID = (M_MIN + M_MAX) / 2
I_MID = (I_MIN + I_MAX) / 2
T_R = T_MAX - T_MIN
M_R = M_MAX - M_MIN
I_R = I_MAX - I_MIN

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
xPos, yPos = 500, 500
p, r, p2, r2, h = 500, 500, 500, 500, 500
old_p = p
old_r = r
old_p2 = p2
old_r2 = r2
old_h = h
while True:
    weight = SENS.read_u16() * 30/65535 # responsiveness
    p2 = []
    r2 = []
    h = []
    for i in range(SAMPLES): # sample multiple times, then take the average
        p2.append((INDEX.read_u16() - I_MIN) * 999/I_R)
        r2.append((MIDDLE.read_u16() - M_MIN) * 999/M_R)
        h.append(999 - (THUMB.read_u16() - T_MIN) * 999/T_R)
        utime.sleep(0.05/SAMPLES)
    p2 = sum(p2)/len(p2)
    r2 = sum(r2)/len(r2)
    h = sum(h)/len(h)
    p2 = int((p2 + weight * old_p2)/(weight + 1)) # slows response for smoother movement
    r2 = int((r2 + weight * old_r2)/(weight + 1))
    h = int((h + weight * old_h)/(weight + 1))
    gyros = mpu.read_gyro_data() # read the gyro
    #print(gyros)
    if abs(gyros['x'] + 2) > 2:
        xPos +=(gyros['x'] + 2)/1.5
    if abs(gyros['y']) > 2:
        yPos += gyros['y']
    accel = mpu.read_accel_data() # read the accelerometer [ms^-2]
    aZ = accel["z"]
    if aZ == 0.0:
        while True:
            try:
                mpu = MPU6050()
                break
            except:
                utime.sleep(.1)
                print("error")
    if aZ < -11: xPos, yPos = 500, 500
    p, r = xPos, 999 - yPos
    p = int((p + weight * old_p)/(weight + 1)) # slows response for smoother movement
    r = int((r + weight * old_r)/(weight + 1))
    if JCS: send(p, r, p - (999 - p2) + 500, 999 - r - r2 + 500, h)
    else: send(p, r, p2, 999 - r2, h)
    old_p2 = p2
    old_r2 = r2
    old_p = p
    old_r = r
    old_h = h
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