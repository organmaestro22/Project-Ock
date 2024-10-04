# Example code for (GY-521) MPU6050 Accelerometer/Gyro Module
# Write in MicroPython by Warayut Poomiwatracanont JAN 2023

from MPU6050 import MPU6050

from os import listdir, chdir
from machine import Pin
from time import sleep_ms
from math import degrees

mpu = MPU6050(sda = 26, scl = 27, addr= 0x68)
xpos = 0
gyro = mpu.read_gyro_data()   # read the gyro [deg/s]
xOff = (gyro["x"])
print(xOff)
while True:
    # Accelerometer Data
    accel = mpu.read_accel_data() # read the accelferometer [ms^-2]
    aX = accel["x"]
    aY = accel["y"]
    aZ = accel["z"]
    #print(aZ)
    #print("x: " + str(aX) + " y: " + str(aY) + " z: " + str(aZ))

    # Gyroscope Data
    gyro = mpu.read_gyro_data()   # read the gyro [deg/s]
    print(gyro["y"])
    gY = gyro["y"]
    gZ = gyro["z"]
    #print("x:" + str(xpos) + " y:" + str(gY) + " z:" + str(gZ))
    angle = mpu.read_angle()
    #print(f"x: {degrees(angle['x'])}, y: {degrees(angle['y'])}")
    # Rough Temperature
    temp = mpu.read_temperature()   # read the device temperature [degC]
    # print("Temperature: " + str(temp) + "°C")

    # G-Force
    # gforce = mpu.read_accel_abs(g=True) # read the absolute acceleration magnitude
    # print("G-Force: " + str(gforce))

    # Write to file
    data = {"Temp" : temp,
            "AcX" : aX,
            "AcY" : aY,
            "AcZ" : aZ
    }
    
    # Time Interval Delay in millisecond (ms)
    sleep_ms(100)