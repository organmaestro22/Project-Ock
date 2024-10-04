import utime
from machine import Pin
class Stepper:
    def __init__(self, pins: [int, int, int, int],
                 step_angle: float = 5.625/32,
                 endstop: int = None,
                 homing_dir: int = None,
                 homing_step_delay: float = 0.002,
                 endstop_pressed_state: int = 1,
                 step_sequence = [[1, 0, 0, 1],  [1, 1, 0, 0], [ 0, 1, 1, 0], [0, 0, 1, 1]]): 
        self.pins = []
        for pin in pins:
            self.pins.append(Pin(pin,Pin.OUT))
        self.stp_angle = step_angle    
        self.limit = endstop
        self.hdir = homing_dir
        self.hsd = homing_step_delay
        self.hval = endstop_pressed_state
        self.stp_seq = step_sequence
        self.stp_index = 0
        self.pos = 0 # keeps track of the steppers position
        
    def enable(self):
        for j in range(4): # output values to the pins
            self.pins[j].value(self.stp_seq[self.stp_index][j])
            
    def disable(self):
        for pin in self.pins:
            pin.value(0)
            
    def setzero(self):
        self.pos = 0
        
    def step(self, steps, delay):
        self.enable()
        for i in range(abs(steps)):
            self.stp_index += round(abs(steps)/steps)
            self.pos += round(abs(steps)/steps) # keep track of the steppers position
            if self.stp_index > 3:
                self.stp_index = 0
            elif self.stp_index < 0:
                self.stp_index = 3
            for j in range(4):# output values to the pins
                self.pins[j].value(self.stp_seq[self.stp_index][j])
            utime.sleep(delay)
    
    def angle(self, angle, delay):
        steps = (-angle)/self.stp_angle - self.pos # calculate the ammount of steps needed to get to the desired angle
        self.step(steps, delay)
        
    def home(self):
        if self.limit == None:
            raise RuntimeError("You must have an enstop to home")
        else:
            homed = False
            while homed == False: # turn until it hits the limit
                if self.limit.value() == self.hval:
                    self.setzero()
                    homed = True
                else:
                    self.step(self.hdir, self.hsd)

def main():
    from random import randint
    
    STP_DELAY = 0.002
    motor = Stepper([12,13,14,15])
    
    while True:
        motor.angle(90,STP_DELAY)
        utime.sleep(1)
        motor.angle(180,STP_DELAY)
        utime.sleep(1)
        