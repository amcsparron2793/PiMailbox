#! python3

"""
VolumeControlNotClass.py

sudo pip3 install adafruit-circuitpython-mcp3xxx
needs to be run for this to work.

THIS WILL ONLY WORK ON RaspberryPi OS LITE 32 Bit as of 2/20/22
"""

import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# create the spi bus - this is for the ADC chip
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select) - this is for the ADC chip
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object - create the chip object itself
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)

# works great as an init check.
print('Raw ADC Value: ', chan0.value)
print('ADC Voltage: ' + str(chan0.voltage) + 'V')

# to keep from being jittery we'll only change
# volume when the pot has moved a significant amount
# on a 16-bit ADC
tolerance = 250


def remap_range(value, left_min, left_max, right_min, right_max):
    """ This remaps a value from original (left) range to new (right) range. """

    # Figure out how 'wide' each range is
    left_span = left_max - left_min
    right_span = right_max - right_min

    # Convert the left range into a 0-1 range (int)
    valueScaled = int(value - left_min) / int(left_span)

    # Convert the 0-1 range into a value in the right range.
    return int(right_min + (valueScaled * right_span))


def WatchVol():
    """ Infinite loop to read and change volume
    using a Pot and an ADC (mcp3008)."""

    # this keeps track of the last potentiometer value
    global last_read
    last_read = 0

    while True:
        # we'll assume that the pot didn't move
        trim_pot_changed = False

        # read the analog pin
        trim_pot = chan0.value

        # how much has it changed since the last read?
        pot_adjust = abs(trim_pot - last_read)

        if pot_adjust > tolerance:
            trim_pot_changed = True

        if trim_pot_changed:
            # convert 16bit adc0 (0-65535) trim pot read into 0-100 volume level
            set_volume = remap_range(trim_pot, 0, 65535, 0, 100)

            # set OS volume playback volume
            print('Volume = {volume}%'.format(volume=set_volume))
            set_vol_cmd = ('sudo amixer cset numid=1 -- {volume}% > /dev/null'.format(volume=set_volume))
            os.system(set_vol_cmd)

            # save the potentiometer reading for the next loop
            last_read = trim_pot

        # hang out and do nothing for a half second
        time.sleep(0.5)


if __name__ == "__main__":
    WatchVol()
