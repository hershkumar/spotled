try:
    import RPi.GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpigpio.utils
    fake_rpigpio.utils.install()
import enum
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
        self.G_PWM = RPi.GPIO.PWM(R_CHANNEL, 100)
        self.B_PWM = RPi.GPIO.PWM(R_CHANNEL, 100)

    def set_led_brightness(self, pwm_object, val):
        if val < 0:
            val = 0
        if val > 100:
            val = 100
        pwm_object.ChangeDutyCycle(val)       

    def change_mode(self, new_mode):
        self.current_mode = new_mode

    def __run__(self):
        while True:
            if self.current_mode is not LedMode.STATIC:            
                for brightness in range(0, 101):
                    self.set_led_brightness(self.R_PWM, self.current_mode(brightness))
                    self.set_led_brightness(self.G_PWM, self.current_mode(brightness))
                    self.set_led_brightness(self.B_PWM, self.current_mode(brightness))
                    sleep(self.UPDATE_RATE)
        self.set_led_brightness(self.R_PWM, 0)
        self.set_led_brightness(self.G_PWM, 0)
        self.set_led_brightness(self.B_PWM, 0)
        RPi.GPIO.cleanup()
