#! python3

"""
*** Adafruit i2C Backpack Setup ***

To set the lcd up correctly,
download https://github.com/adafruit/Adafruit_CircuitPython_CharLCD.git
install adafruit-circuitpython-charlcd.
To test i2c functionality make sure i2C and spi are enabled in raspi-config.
"""

import board
import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd
from time import sleep

# specify the size of the LCD
cols = 16
rows = 2

# setup the i2c bus with the SCL and SDA pins
i2c = busio.I2C(board.SCL, board.SDA)

# create an lcd instance using the i2c bus that was set up above
lcd = character_lcd.Character_LCD_I2C(i2c, cols, rows)

# print hello, sleep and clear the screen
lcd.message("hello")
sleep(5)
lcd.clear()

# turn lcd off
sleep(1)
lcd.backlight(100)
