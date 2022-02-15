#! python3
"""
MechClassesPi.py

if I can get the monitor running on the raspberry pi,
then all the programming for the mechanical side of things would be done here.

as of 2/6/22 10am default pins are servo = 22, pwr_led = 16, mail_led = 20
as of 2/6/22 11am default for reset_button_pin = 12

"""

# imports
from os import system
from os.path import isfile
from time import sleep

import gpiozero
import threading
import Adafruit_CharLCD as LCD


class MailBoxLCD:
    def __init__(self, lcd_columns=16, lcd_rows=2):
        # Define LCD column and row size for 16x2 LCD.
        self.lcd_columns = lcd_columns
        self.lcd_rows = lcd_rows

        # Initialize the LCD using the pins
        try:
            self.lcd = LCD.Adafruit_CharLCDBackpack()
            print("LCD initialized")
        except Exception as e:
            print(f"Error: {e}")

    def on(self):
        # Turn backlight on
        self.lcd.set_backlight(0)

    def clear(self):
        # Clear the LCD
        self.lcd.clear()

    def off(self):
        # Turn the backlight off
        self.lcd.clear()
        self.lcd.set_backlight(100)

    def write_message(self, msg_text):
        self.lcd.message(msg_text)


class Mechanics:
    def __init__(self, servo_pin, pwr_led_pin,
                 mail_led_pin, reset_button_pin, fault_LED_pin):
        # TODO: error handling
        # TODO: docstrings
        self.mp3_path = "../Misc_Project_Files/youve-got-mail-sound.mp3"
        self.mp3_path_backup = "./youve-got-mail-sound.mp3"
        self.mp3_command = None

        self.servo = gpiozero.Servo(servo_pin)
        self.reset_btn = gpiozero.Button(reset_button_pin)

        self.power_led = gpiozero.LED(pwr_led_pin)
        self.mail_led = gpiozero.LED(mail_led_pin)
        self.fault_led = gpiozero.LED(fault_LED_pin)

        self.servo_up = None
        self.pwr_on = None
        self.mail_on = None
        self.fault_on = None
        self.lcd_on = None

        self.PowerOn()

        # TODO: sound v2 with py module instead of system(vlc)?
        self.mp3_path, self.sound_state = self.mp3Init()

        self.lcd = MailBoxLCD()

        # set up a thread for self.ResetWatcher
        self.reset_thread = threading.Thread(target=self.ResetWatcher)

    def lcdGotMail(self):
        self.lcd.on()
        # TODO: add in from: xxx
        self.lcd.write_message("You've got mail!")
        has_message = True
        sleep(2)
        return has_message

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
        self.fault_led.blink(n=1)
        return self.pwr_on

    def YouGotMail(self):
        if not self.servo_up:
            if self.sound_state:
                # plays youve-got-mail-sound.mp3 and immediately exits vlc
                try:
                    system(f"vlc -q --play-and-exit {self.mp3_path}")
                    # system(f"{self.mp3_path}")
                    raise Exception("this is a test")
                except Exception as e:
                    self.FaultOn()
                    print(f"ERROR: {e}")
                    pass
            else:
                pass
        else:
            pass

        # if the servo is already up, pass, otherwise run self.FlagUp()
        if self.servo_up:
            pass
        else:
            self.FlagUp()
            self.lcd_on = self.lcdGotMail()

        # if the mail led is already on, pass, otherwise run self.MailOn()
        if self.mail_on:
            pass
        else:
            self.MailOn()

        # run the reset thread that was set up in init
        if not self.reset_thread.isAlive():
            try:
                self.reset_thread.start()
            except RuntimeError:
                self.reset_thread = threading.Thread(target=self.ResetWatcher)
                self.reset_thread.start()
        else:
            pass

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

    def FaultOn(self):
        self.fault_led.blink()
        self.fault_on = True
        return self.fault_on

    def FaultOff(self):
        self.fault_led.off()
        self.fault_on = False
        return self.fault_on

    def Reset(self):
        if self.mail_on:
            self.MailOff()
        else:
            pass

        if self.servo_up:
            self.FlagDown()
        else:
            pass

        if self.lcd_on:
            self.lcd.off()
        else:
            pass

        if self.fault_on:
            self.fault_led.off()
        else:
            pass

    def ResetWatcher(self):
        while True:
            if self.reset_btn.is_pressed:
                print("Resetting...")
                self.Reset()
                sleep(5)
                break
            else:
                sleep(1)
        if not self.reset_thread.isAlive():
            try:
                self.reset_thread.start()
            except RuntimeError:
                self.reset_thread = threading.Thread(target=self.ResetWatcher)
                # self.reset_thread.start()
        else:
            pass


# TODO: remove this when not testing pi

if __name__ == "__main__":
    m = Mechanics(22, 16, 20, 12, 6)
    while True:
        m.YouGotMail()
        sleep(2)
