from machine import Pin, ADC, PWM

s = 3
THUMB = ADC(Pin(34)) # CONTROLL STICKS
MIDDLE = ADC(Pin(32))
INDEX = ADC(Pin(39))
MOT = PWM(Pin(27))
THUMB.atten(ADC.ATTN_11DB) # attenuation for 3lk.3V
MIDDLE.atten(ADC.ATTN_11DB)
INDEX.atten(ADC.ATTN_11DB)

# Calibration
SAMPLES = 100 # number of samples to take of sensor reading per command send
M_MIN = 27000
M_MAX = 41000
I_MIN = 37000
I_MAX = 45000
T_MIN = 23000
T_MAX = 40000
T_MID = (T_MIN + T_MAX) / 2
M_MID = (M_MIN + M_MAX) / 2
I_MID = (I_MIN + I_MAX) / 2
T_R = T_MAX - T_MIN
M_R = M_MAX - M_MIN
I_R = I_MAX - I_MIN
print(I_MIN)
while True:
    if s == 1:
        t1 = THUMB.read_u16()
        t2 = t1 - T_MIN
        t3 = t2 * 999/T_R
        print(t1, t2, t3)
    elif s == 2:
        t1 = INDEX.read_u16()
        t2 = t1 - I_MIN
        t3 = t2 * 999/I_R
        print(t1, t2, t3)
    else:
        t1 = MIDDLE.read_u16()
        t2 = t1 - M_MIN
        t3 = t2 * 999/M_R
        print(t1, t2, t3)
        MOT.duty_u16(MIDDLE.read_u16())