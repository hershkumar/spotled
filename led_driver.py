try:
    import RPi.GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpigpio.utils
    fake_rpigpio.utils.install()
import enum
import math
from threading import Thread
from time import sleep

class LedColor():
    h_val, s_val, v_val = 0, 0, 0

    def rgb_to_hsv(self, r, g, b):
        rgb_values = [r/255.0, g/255.0, b/255.0]
        conversion_constants = [((rgb_values[1] - rgb_values[2]), 360), 
                                ((rgb_values[2] - rgb_values[0]), 120),
                                ((rgb_values[0] - rgb_values[1]), 240)]

        max_color_index = rgb_values.index(max(rgb_values)) 
        min_color_index = rgb_values.index(min(rgb_values))
        diff = rgb_values[max_color_index] - rgb_values[min_color_index] 

        if rgb_values[max_color_index] == rgb_values[min_color_index]:
            h_val = 0
        else:
            h_val = (60 * (conversion_constants[max_color_index][0] / diff) + conversion_constants[max_color_index][1]) % 360

        if rgb_values[max_color_index] == 0:
            s_val = 0
        else:
            s_val = (diff / rgb_values[max_color_index]) * 100
        
        v_val = rgb_values[max_color_index] * 100

        return (round(h_val), round(s_val), round(v_val))

    #this is broken dont use it yet
    def hsv_to_rgb(self):
        h_val, s_val, v_val = self.h_val, self.s_val/100., self.v_val/100.
        i = math.floor((h_val) * 6)
        f = h_val * 6 - i
        p = v_val * (1 - s_val)
        q = v_val * (1 - f * s_val)
        t = v_val * (1 - (1 - f) * s_val)

        rgb_combos = [(v_val, t, p), 
                        (q, v_val, p), 
                        (p, v_val, t), 
                        (p, q, v_val), 
                        (t, p, v_val), 
                        (v_val, p, q)]

        rgb_val = rgb_combos[i % 6]
        return (round(rgb_val[0] * 255), 
                round(rgb_val[1] * 255), 
                round(rgb_val[2] * 255))

class LedMode(enum.Enum):
    #function of brightness over time as a lambda
    STATIC = lambda brightness: brightness,
    BEATHING = lambda brightness: ()

class LedDriver(Thread):

    UPDATE_RATE = 1 / 30 #hz

    def __init__(self, R_CHANNEL, G_CHANNEL, B_CHANNEL):
        self.current_mode = LedMode.STATIC

        RPi.GPIO.setmode(RPi.GPIO.BOARD)
        RPi.GPIO.setup(R_CHANNEL, RPi.GPIO.OUT)
        RPi.GPIO.setup(G_CHANNEL, RPi.GPIO.OUT)
        RPi.GPIO.setup(B_CHANNEL, RPi.GPIO.OUT)

        self.R_PWM = RPi.GPIO.PWM(R_CHANNEL, 100)
        self.G_PWM = RPi.GPIO.PWM(G_CHANNEL, 100)
        self.B_PWM = RPi.GPIO.PWM(B_CHANNEL, 100)

        self.R_PWM.start(0)
        self.G_PWM.start(0)
        self.B_PWM.start(0)
    
    def set_rgb_power(self, rgb_vals):
        self.R_PWM.ChangeDutyCycle(rgb_vals[0]/255.)
        self.G_PWM.ChangeDutyCycle(rgb_vals[1]/255.)
        self.B_PWM.ChangeDutyCycle(rgb_vals[2]/255.) 

    def change_mode(self, new_mode):
        self.current_mode = new_mode

    # def __run__(self):
    #     while True:
    #         if self.current_mode is not LedMode.STATIC:            
    #             for brightness in range(0, 101):
                    #todo: something eventually
    #     RPi.GPIO.cleanup()

driver = LedDriver(17, 22, 24)
LedDriver.set_rgb_power((255,255,0))