#! python3

"""
WaitForEnable.py

This module initializes the Enable Button and waits for a press.
When that happens, it calls runs system("python3 MailMonitorSMTP.py").

"""

from time import sleep
from os import system

from gpiozero import Button

enable_button = Button(25)


# functions
def WaitForEnable():
    """ Checks if enable_button was pressed,
     and calls system("python3 MailMonitorSMTP.py") if it was.
     Otherwise, the program sleeps for 0.5 seconds."""

    while True:
        try:
            if enable_button.is_pressed:
                system("python3 MailMonitorSMTP.py")
                break
            else:
                sleep(0.5)
            print("Goodbye!")
            #exit()
        except KeyboardInterrupt:
            print("Goodbye!")
            exit()


if __name__ == "__main__":
    WaitForEnable()
