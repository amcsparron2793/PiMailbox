#! python3

"""
WaitForEnable.py

This module initializes the Enable Button and waits for a press.
When that happens, it runs mm.NewEmailWatcher.

"""

from time import sleep
from os import system

from gpiozero import Button
import MailMonitorSMTP as mm
enable_button = Button(25)


# functions
def WaitForEnable():
    """ Checks if enable_button was pressed.
     When that happens, it runs mm.NewEmailWatcher.
     Otherwise, the program sleeps for 0.5 seconds."""

    print("\n**** Standing By For Enable Button Press ****\n")
    while True:
        try:
            if enable_button.is_pressed:
                mm.NewEmailWatcher()
                #system("python3 MailMonitorSMTP.py")
                break
            else:
                sleep(0.5)
        except KeyboardInterrupt:
            print("Goodbye!")
            exit()
        except Exception as e:
            mm.Mech.FaultOn()
            raise e


if __name__ == "__main__":
    WaitForEnable()
