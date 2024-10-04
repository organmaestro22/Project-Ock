from machine import Pin, ADC, PWM
import utime
from MPU6050 import MPU6050

class PowerHand:
    """
    Class for a 7 axis 1 button hand controller with a vibration motor. Contains 5 flex sensors and 1 MPU (reads 2 axes).
    Optional Haptic feebcack with using the vibration motor, otherwise leave that pin undefined
    """
    def __init__(self, **kwargs):
        # Finger Flex Sensors
        self.THUMB = ADC(Pin(kwargs['thumb']))
        self.INDEX = ADC(Pin(kwargs['index']))
        self.MIDDLE = ADC(Pin(kwargs['middle']))
        self.RING = ADC(Pin(kwargs['ring']))
        self.PINKY = ADC(Pin(kwargs['pinky']))
        self.THUMB.atten(ADC.ATTN_11DB) # attenuation for 3.3V
        self.MIDDLE.atten(ADC.ATTN_11DB)
        self.INDEX.atten(ADC.ATTN_11DB)
        self.RING.atten(ADC.ATTN_11DB)
        self.PINKY.atten(ADC.ATTN_11DB)

        # MPU
        self.SCL = kwargs['scl']
        self.SDA = kwargs['sda']
        self.MPU = MPU6050(scl = self.SCL, sda = self.SDA, addr = kwargs['addr'])
        self.xPos = 0
        self.yPos = 0


        # Calibration
        self.MPU_FLAT_ACCEL = kwargs['mpu_flat_accel']
        
        # Optional Haptic Feedback
        try:
            self.VMOT = PWM(Pin(kwargs['vmot']))
            self.VMOT.duty_u16(0)
            self._VMOT_ENABLED = True
        except:
            self._VMOT_ENABLED = False

        # Thumb Button
        self.BUTTON = Pin(kwargs['button'], Pin.IN)

    def read(self, time, samples):
        """Read all sensor values

        Args:
            time (int): Duration in seconds to sample the flex sensors
            samples (int): Samples to take of flex sensor values

        Returns:
            dict: Sensor values mapped to: thumb, index, middle, ring, pinky, x, y
        """
        # read the sensors multiple times and take the average (reduces jitter)
        t, i, m, r, p = 0, 0, 0, 0, 0
        for k in range(samples):
            t += self.THUMB.read_u16()
            i += self.INDEX.read_u16()
            m += self.MIDDLE.read_u16()
            r += self.RING.read_u16()
            p += self.PINKY.read_u16()
            utime.sleep(time/samples)
        t /= samples
        i /= samples
        m /= samples
        r /= samples
        p /= samples
        
        # read the button
        b = self.BUTTON.value()

        # read the MPU
        gyros = self.MPU.read_gyro_data() # read the gyro
        if abs(gyros['x']) > 2: # cuts out low values
            self.xPos +=(gyros['x']+.5) # MPU usually reads this as -2, so the +2 is a calibration
        if abs(gyros['y']+3.5) > 2:
            self.yPos += gyros['y'] + 3.5
        accel = self.MPU.read_accel_data() # read the accelerometer [ms^-2]
        aZ = accel["z"]
        if aZ == 0.0: # reinitialize the MPU if it dissconects
            print("wiring unstable")
            while True: # keep trying to reinit the MPU and print an error everytime it fails
                try:
                    self.MPU = MPU6050(scl = self.SCL, sda = self.SDA)
                    break
                except:
                    utime.sleep(.1)
                    print("error")
        if aZ < self.MPU_FLAT_ACCEL: self.xPos, self.yPos = 0, 0
        return {"thumb": t, "index": i, "middle": m, "ring": r, "pinky": p, "button": b, "x": self.xPos, "y": self.yPos}
    
    def hapticFeedback(self, strength):
        """Give haptic feedback usingd the vibration motor

        Args:
            strength (int): 0-65535
        """
        if self._VMOT_ENABLED:
            self.VMOT.duty_u16(strength)
        else: print("No motor attached")

if __name__ == "__main__":
    hand = PowerHand(addr = 0x68, thumb = 33, index = 39, middle = 34, ring = 35, pinky = 32, sda = 26, scl = 27, vmot = 14, mpu_flat_accel = -4,  button = 25)
    while True: print(hand.read(.05, 100))