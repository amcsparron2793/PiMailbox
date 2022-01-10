#! python3
"""
MechClassesPi.py

if i can get the monitor running on the raspberry pi,
then all the programming for the mechanical side of things would be done here.
"""

# imports
import gpiozero


class Mechanics:
    def __init__(self, servo_pin, pwr_led_pin, mail_led_pin):
        # TODO: testing and error handling
        self.servo = gpiozero.Servo(servo_pin)
        self.power_led = gpiozero.LED(pwr_led_pin)
        self.mail_led = gpiozero.LED(mail_led_pin)
        self.servo_up = None
        self.pwr_on = None
        self.mail_on = None
        self.PowerOn()

    def PowerOn(self):
        """Turns the External PowerLED LED on."""
        self.power_led.on()
        self.pwr_on = True
        return self.pwr_on

    def YouGotMail(self):
        if self.servo_up:
            pass
        else:
            self.FlagUp()

        if self.mail_on:
            pass
        else:
            self.MailOn()

    def FlagUp(self):
        self.servo.max()
        self.servo_up = True
        return self.servo_up

    def FlagDown(self):
        self.servo.min()
        self.servo_up = False
        return self.servo_up

    def MailOn(self):
        self.mail_led.blink()
        self.mail_on = True
        return self.mail_on

    def MailOff(self):
        self.mail_led.off()
        self.mail_on = False
        return self.mail_on

    def Reset(self):
        if self.mail_on:
            self.MailOff()
        else:
            pass

        if self.servo_up:
            self.FlagDown()
        else:
            pass
