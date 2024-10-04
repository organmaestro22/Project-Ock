
"""# Import socket module 
import socket             
 
# Create a socket object 
s = socket.socket()         
 
# Define the port on which you want to connect 
port = 80               
 
# connect to the server on local computer 
s.connect(('192.168.4.1', port)) 
 
# receive data from the server and decoding to get the string.
while True:
    print (s.recv(1024).decode())
    s.send(input("message: ").encode())
# close the connection 
s.close()     """
import socket
import time
class CompClient:
    def __init__(self, ip:str, port = 80):
        self.sock = socket.socket()
        self.port = port
        self.ip = ip

    def send(self, msg): # send a message to the esp32
        self.sock.send(msg.encode())

    def quit(self):
        self.send("quit")
        self.sock.close()
        
    def receive(self):
        res = self.sock.recv(1024).decode()
        if res == "quit": self.sock.close(); return False
        return res
    
    def connect(self): # Ccnnect to the esp32
        self.sock.connect((self.ip, self.port))
        self.send("init")
        if self.receive() == "ready":
            return True
        else:
            return False
    
test = CompClient('192.168.4.1')
test.connect()
test.send(input("msg: "))
while test.receive():
    time.sleep(0.1)
    test.send("1111")
    test.receive()
    time.sleep(0.1)
    test.send("0000")
    test.receive()
    time.sleep(0.1)
    test.send("1111")
    test.receive()
    time.sleep(0.1)
    test.send("0000")

