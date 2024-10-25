class Platform:
    def __init__(self, motor_a, motor_b, motor_c, a_min, a_max, b_min, b_max, c_min, c_max, RATIO):
        self.a_mot = motor_a
        self.b_mot = motor_b
        self.c_mot = motor_c
        self.mots = [self.a_mot, self.b_mot, self.c_mot]
        self.a_min = a_min
        self.a_max = a_max
        self.b_min = b_min
        self.b_max = b_max
        self.c_min = c_min
        self.c_max = c_max
        self.mot_set_pos = [0, 0, 0]
        self.RATIO = RATIO
    
    def enable(self):
        for mot in self.mots:
            mot.enable()
    
    def disable(self):
        for mot in self.mots:
            mot.disarm()

    def update(self):
        for i in range(3):
            self.mots[i].write(self.mot_set_pos[i]) # set each motor to it's set position

    def setMotors(self, a, b, c): # set the motors to specified angles
        self.mot_set_pos = [a, b, c]

    def getMotorAngles(self, pitch, roll, z):
        a = z * 130/2.125 - pitch * 65/65.492 + 65 # Insert Kinematic equation here
        b = z * 130/2.125 + pitch * 65/65.492 - roll * 65/65.492  + 65 # Insert Kinematic equation here
        c = z * 130/2.125 + pitch * 65/65.492 + roll * 65/65.492 + 65 # Insert Kinematic equation here

        # Limits
        if a > self.a_max: a = self.a_max
        elif a < self.a_min: a = self.a_min
        if b > self.b_max: b = self.b_max
        elif b < self.b_min: b = self.b_min
        if c > self.c_max: c = self.c_max
        elif c < self.c_min: c = self.c_min
        
        return [a, b, c]
    
    def setPos(self, pitch, roll, z):
        angles = self.getMotorAngles(pitch, roll, z)
        self.mot_set_pos = angles
    
    def moveTo(self, pitch, roll, z):
        self.setPos(pitch, roll, z)
        self.update()