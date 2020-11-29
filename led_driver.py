try:
    import RPi.GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpigpio.utils
    fake_rpigpio.utils.install()
import enum
from threading import Thread
from time import sleep

class LedMode(enum.Enum):
    #function of brightness over time as a lambda
    STATIC = lambda brightness: brightness,
    BEATHING = lambda brightness: (),
    RAINBOW = 2,
    BLINKING = 3,
    MORSE = 4

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
        self.set_LED_brightness(self.R_PWM, 40)

    def set_LED_brightness(self, pwm_object, val):
        if val < 0:
            val = 0
        if val > 100:
            val = 100
        pwm_object.ChangeDutyCycle(val)       

    def change_mode(self, new_mode):
        self.current_mode = new_mode

    def __run__(self):
        while True:
            for brightness in range(0, 101):
                if self.current_mode is not LedMode.STATIC:
                    self.current_mode(brightness)
                    sleep(self.UPDATE_RATE)
        self.set_LED_brightness(self.R_PWM, 0)
        self.set_LED_brightness(self.G_PWM, 0)
        self.set_LED_brightness(self.B_PWM, 0)
        RPi.GPIO.cleanup()
