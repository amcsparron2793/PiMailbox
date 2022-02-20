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

i2c = busio.I2C(board.SCL, board.SDA)
cols = 16
rows = 2
lcd = character_lcd.Character_LCD_I2C(i2c, cols, rows)
lcd.message("hello")
sleep(5)
lcd.clear()
# lcd is off
lcd.backlight(100)
