#! python3

from time import sleep
# start of low level i2c/sci modules from adafruit
# noinspection PyUnresolvedReferences
import Adafruit_CharLCD as LCD
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


class ADCChipInit:
    def __init__(self, cs_board_pin: board):
        # These are never used outside the __init__ method,
        # so they don't need to be self.xxx
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        # create the cs (chip select) - this is for the ADC chip
        cs = digitalio.DigitalInOut(cs_board_pin)
        # create the mcp object - create the chip object itself
        mcp = MCP.MCP3008(spi, cs)

        # create an analog input channel on pin 0
        self.chan0 = AnalogIn(mcp, MCP.P0)

        # works great as an init check.
        print('Raw ADC Value: ', self.chan0.value)
        print('ADC Voltage: ' + str(self.chan0.voltage) + 'V')
        self.threshold = 250

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

    def ReadPotValue(self):
        # this keeps track of the last potentiometer value
        last_read = 0

        while True:
            # we'll assume that the pot didn't move
            trim_pot_changed = False

            # read the analog pin
            trim_pot = self.chan0.value

            # how much has it changed since the last read?
            pot_adjust = abs(trim_pot - last_read)

            if pot_adjust > self.threshold:
                trim_pot_changed = True

            if trim_pot_changed:
                # convert 16bit adc0 (0-65535) trim pot read into 0-100 volume level
                trim_pot_value = self._remap_range(trim_pot, 0, 65535, 0, 100)
                print(trim_pot_value)

                # save the potentiometer reading for the next loop
                last_read = trim_pot

            # hang out and do nothing for a half second
            sleep(0.5)


if __name__ == "__main__":
    adc = ADCChipInit(board.D22)
    adc.ReadPotValue()
