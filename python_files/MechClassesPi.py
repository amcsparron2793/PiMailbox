#! python3
"""
MechClassesPi.py

if I can get the monitor running on the raspberry pi,
then all the programming for the mechanical side of things would be done here.

as of 2/6/22 10am default pins are servo = 22, pwr_led = 16, mail_led = 20
as of 2/6/22 11am default for reset_button_pin = 12
as of 2/15/22 default for fault_led_pin = 6
as of 2/20/22 default pins are servo = 17, pwr_led = 16, mail_led = 20
"""

# imports
from os import system
from os.path import isfile
from time import sleep

import gpiozero
import threading

# start of low level i2c/sci modules from adafruit
# noinspection PyUnresolvedReferences
import Adafruit_CharLCD as LCD
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


class VolumeControl:
    """Allows for pot based volume control using an MCP3008 ADC Chip."""
    def __init__(self):
        # These are never used outside the __init__ method,
        # so they don't need to be self.xxx
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        # create the cs (chip select) - this is for the ADC chip
        cs = digitalio.DigitalInOut(board.D22)
        # create the mcp object - create the chip object itself
        mcp = MCP.MCP3008(spi, cs)

        # create an analog input channel on pin 0
        self.chan0 = AnalogIn(mcp, MCP.P0)

        # works great as an init check.
        print('Raw ADC Value: ', self.chan0.value)
        print('ADC Voltage: ' + str(self.chan0.voltage) + 'V')

        # to keep from being jittery we'll only change
        # volume when the pot has moved a significant amount
        # on a 16-bit ADC
        self.tolerance = 250

    @staticmethod
    def _remap_range(value, left_min, left_max, right_min, right_max):
        """ This remaps a value from original (left) range to new (right) range. """

        # Figure out how 'wide' each range is
        left_span = left_max - left_min
        right_span = right_max - right_min

        # Convert the left range into a 0-1 range (int)
        value_scaled = int(value - left_min) / int(left_span)

        # Convert the 0-1 range into a value in the right range.
        return int(right_min + (value_scaled * right_span))

    def WatchVol(self):
        """ Infinite loop to read and change volume
        using a Pot and an ADC (mcp3008)."""

        # this keeps track of the last potentiometer value
        last_read = 0

        while True:
            # we'll assume that the pot didn't move
            trim_pot_changed = False

            # read the analog pin
            trim_pot = self.chan0.value

            # how much has it changed since the last read?
            pot_adjust = abs(trim_pot - last_read)

            if pot_adjust > self.tolerance:
                trim_pot_changed = True

            if trim_pot_changed:
                # convert 16bit adc0 (0-65535) trim pot read into 0-100 volume level
                set_volume = self._remap_range(trim_pot, 0, 65535, 0, 100)

                # set OS volume playback volume
                # print('Volume = {volume}%'.format(volume=set_volume))
                set_vol_cmd = ('sudo amixer cset numid=1 -- {volume}% > /dev/null'.format(volume=set_volume))
                system(set_vol_cmd)

                # save the potentiometer reading for the next loop
                last_read = trim_pot

            # hang out and do nothing for a half second
            sleep(0.5)


class MailBoxLCD:
    def __init__(self, lcd_columns=16, lcd_rows=2):
        # Define LCD column and row size for 16x2 LCD.
        self.lcd_columns = lcd_columns
        self.lcd_rows = lcd_rows

        # Initialize the LCD using the pins
        try:
            self.lcd = LCD.Adafruit_CharLCDBackpack()
            print("LCD initialized")
            self.lcd.message("LCD initialized")
            sleep(3)
            self.lcd.clear()
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
        if len(msg_text) > 16:
            self.lcd.message(f"{msg_text[0:17]}\n{msg_text[17:]}")
        else:
            self.lcd.message(msg_text)

    def write_error(self, err_text):
        err_text = ("Error: " + str(err_text))
        if len(err_text) > 16:
            self.lcd.message(f"{err_text[0:17]}\n{err_text[17:]}")
        else:
            self.lcd.message(err_text)
        # self.FaultOn()


class Mechanics:
    def __init__(self, servo_pin, pwr_led_pin,
                 mail_led_pin, reset_button_pin, fault_LED_pin):
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
        try:
            self.lcd = MailBoxLCD()
            self.vol = VolumeControl()
        except Exception as e:
            self.FaultOn()
            print(f"Error: {e}")

        # set up a thread for self.ResetWatcher
        self.reset_thread = threading.Thread(target=self.ResetWatcher)
        self.vol_thread = threading.Thread(target=self.vol.WatchVol)
        self.vol_thread.start()

    def FullErrHandle(self, err):
        self.lcd.on()
        self.lcd.write_error(str(err.args[0]))
        self.FaultOn()
        print(f"ERROR: {err}")

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
                except Exception as e:
                    self.FullErrHandle(e)
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
        if not self.reset_thread.is_alive():
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
        if not self.reset_thread.is_alive():
            try:
                self.reset_thread.start()
            except RuntimeError:
                self.reset_thread = threading.Thread(target=self.ResetWatcher)
                # self.reset_thread.start()
        else:
            pass


# TODO: remove this when not testing pi

if __name__ == "__main__":
    m = Mechanics(17, 16, 20, 12, 6)
    while True:
        m.YouGotMail()
        sleep(2)
