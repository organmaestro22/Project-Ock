from servo import Servo

class EndEffector:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def setServos(self, a, b):
        self.a.write(a)
        self.b.write(b)
    
    def getAngles(self, b, t):
        aPos = 90 + t - b
        bPos = t + b
        return aPos, bPos
    
    def moveTo(self, b, t):
        a, b = self.getAngles(b, t)
        self.setServos(a, b)

EA = Servo(22)
EB = Servo(23)
e = EndEffector(EA,EB)
e.moveTo(90,90)