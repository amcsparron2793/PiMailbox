#! python3
"""
MechClassesPi.py

if I can get the monitor running on the raspberry pi,
then all the programming for the mechanical side of things would be done here.
"""

# imports
from os import system
from os.path import isfile

import gpiozero


class Mechanics:
    def __init__(self, servo_pin, pwr_led_pin, mail_led_pin):
        # TODO: error handling
        # TODO: docstrings
        self.mp3_path = "../Misc_Project_Files/youve-got-mail-sound.mp3"
        self.mp3_path_backup = "./youve-got-mail-sound.mp3"
        self.mp3_command = None

        self.servo = gpiozero.Servo(servo_pin)

        self.power_led = gpiozero.LED(pwr_led_pin)
        self.mail_led = gpiozero.LED(mail_led_pin)

        self.servo_up = None
        self.pwr_on = None
        self.mail_on = None

        self.PowerOn()
        # TODO: sound v2 with py module instead of system()?
        self.mp3_path, self.sound_state = self.mp3Init()

    def mp3Init(self):
        if isfile(self.mp3_path):
            print(f"mp3 detected at {self.mp3_path}")
            use_sound = True
            return self.mp3_path, use_sound
        elif isfile(self.mp3_path_backup):
            print(f"mp3 detected at {self.mp3_path_backup}")
            self.mp3_path = self.mp3_path_backup
            use_sound = True
            return self.mp3_path, use_sound
        else:
            print("mp3 file not found, disabling sound output")
            self.mp3_path = None
            use_sound = False
            return self.mp3_path, use_sound

    def PowerOn(self):
        """Turns the External PowerLED LED on."""
        self.power_led.on()
        self.pwr_on = True
        self.servo.min()
        return self.pwr_on

    def YouGotMail(self):
        if self.sound_state:
            system(f"vlc {self.mp3_path}")
        else:
            pass
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
