from servo import Servo

class EndEffector:
    def __init__(self, a, b):
        self.a = Servo(a)
        self.b = Servo(b)

    def setServos(self, a, b):
        self.a.write(a)
        self.b.write(b)
    
    def getAngles(self, t, b):
        aPos = (t+b)/2
        bPos = (b-t)/2
        return aPos, bPos
    
    def moveTo(self, t, b):
        self.setServos(self.getAngles(t, b))

if __name__ == "__main__":
    test = EndEffector(4, 16)
    test.moveTo(60, 60)
