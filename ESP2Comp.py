"""ssid = 'ESP_AP'
password = '123456789'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid,authmode=network.AUTH_WPA_WPA2_PSK, password=password)

while ap.active() == False:
  pass

print('Connection successful')
print(ap.ifconfig())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
conn, addr = s.accept()
while True:
    
    print('Got a connection from %s' % str(addr))
    cmd = (conn.recv(1024).decode())
    print(cmd)
    conn.send(input("message").encode())
    if cmd == "on":
      Pin(2,Pin.OUT).on()
    if cmd == "off":
      Pin(2,Pin.OUT).off()
    elif cmd == "quit": break
conn.close()"""
import utime
from machine import Pin
class ESP32Server:
    def __init__(self, APSSID, APPWD, PORT = 80):
        try:
            import usocket as socket
        except:
            import socket
        import network
        from machine import Pin
        import esp
        esp.osdebug(None)
        import gc
        gc.collect()
        
        self.AP = network.WLAN(network.AP_IF)
        self.SSID = APSSID
        self.PWD = APPWD
        self.PORT = PORT
        self.AP.active(True)
        self.AP.config(essid=self.SSID,authmode=network.AUTH_WPA_WPA2_PSK, password=self.PWD) # create wifi AP
        while self.AP.active() == False: # wait for AP
          pass
        print(f"IP: {self.AP.ifconfig()[0]}")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def send(self, msg): # send a message to the computer
        self.CONN.send(msg.encode())

    def quit(self): # terminate the socket and AP
        self.send("quit")
        self.CONN.close()
        self.AP.active(False)
        while self.AP.active() == True:
            pass
        print("AP Closed")
        
    def receive(self):
        res = self.CONN.recv(1024).decode()
        if res == "quit": self.quit(); return False
        return res
    
    def connect(self): # Ccnnect to the computer
        self.sock.bind(('', self.PORT))
        self.sock.listen(5)
        self.CONN, self.ADDR = self.sock.accept()
        if self.CONN.recv(1024).decode() == "init":
            self.send("ready")
            return True
        else: return False

test = ESP32Server("ESP_AP", "Alta2023")
connected = test.connect()
cmd = test.receive()
ledPins = [4, 16, 17, 18]
while cmd:
    if cmd == "on":
      Pin(4,Pin.OUT).on()
      Pin(16,Pin.OUT).on()
      Pin(17,Pin.OUT).on()
      Pin(18,Pin.OUT).on()
    elif cmd == "off":
      Pin(4,Pin.OUT).off()
      Pin(16,Pin.OUT).off()
      Pin(17,Pin.OUT).off()
      Pin(18,Pin.OUT).off()
    elif cmd == "quit": break
    else:
        leds = cmd
        for led in range(len(leds)):
            Pin(ledPins[led], Pin.OUT).value(int(leds[led]))
    test.send("ready")
    cmd = test.receive()

        


