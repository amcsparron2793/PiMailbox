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

    def ReadRawValue(self):
        # this keeps track of the last potentiometer value
        last_read = 0

        while True:
            # we'll assume that the pot didn't move
            trim_pot_changed = False

            # read the analog pin
            trim_pot = self.chan0.value

            # how much has it changed since the last read?
            pot_adjust = abs(trim_pot - last_read)

            print(pot_adjust)


if __name__ == "__main__":
    adc = ADCChipInit(board.D22)
    adc.ReadRawValue()
