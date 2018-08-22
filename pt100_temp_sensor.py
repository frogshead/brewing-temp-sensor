# pylint: disable-all
# Disable pylint for micropython project
from machine import Pin, SPI
import time


class MAX31865():
    def __init__(self, clk=14, mosi=13, miso=12,  cs=27):
        self.SCK = Pin(clk, Pin.OUT)
        self.MOSI = Pin(mosi, Pin.OUT)
        self.MISO = Pin(miso, Pin.IN)
        self.CS = Pin(cs, Pin.OUT)
        # HSPI is MOSI=GPIO13, MISO=GPIO12 and SCK=GPIO14
        # HSPI(1)
        self.spi = SPI(1)
        self.spi.init(baudrate=100000, sck=self.SCK,
                      miso=self.MISO, mosi=self.MOSI, polarity = 0, phase = 1)
        """
            Configuration bits:
            Vbias           1=on
            Conversion mode 1=auto,0=normally off
            1-shot          1=1-shot (auto-clear)
            3-wire          1=3-wire,0=2/4 wire
            Fault detection
            Fault detection
            Fault Status    1=clear
            Filter          1=50Hz,2=60Hz
        """
        config = 0xb2
        buf = bytearray(2)
        buf[0] = 0x80  # configuration write addr
        buf[1] = config
        self.CS.value(0)
        self.spi.write(buf)
        self.CS.value(1)
        time.sleep(.2)

    # Re-implementing:
    # https://github.com/frogshead/MAX31865/blob/master/max31865.py
    def read_temperature(self):
        print("Entering read_temp function")
        time.sleep(.2)
        buf = bytearray(1)
        buf[0] = 0x00
        self.CS.value(0)
        self.spi.write(buf)
        register_values = self.spi.read(8)
        self.CS.value(1)
        print("Configuration Register Value: {:02x}".format(register_values[0]))
        print("RTD MSB Register Value: {:02x}".format(register_values[1]))
        print("RTD LSB Register Value: {:02x}".format(register_values[2]))
        print("High Fault MSB Treshold Register Value: {:02x}".format(register_values[3]))
        print("High Fault LSB Treshold Register Value: {:02x}".format(register_values[4]))
        print("Low Fault MSB Register Value: {:02x}".format(register_values[5]))
        print("Low Fault LSB Register Value: {:02x}".format(register_values[6]))
        print("Fault Status Register Value: {:02x}".format(register_values[0]))

        adc = ((register_values[1] << 8) | register_values[2]) >> 1
        print("ADC value: ", adc)
        print("Linear Temperature: {}".format((adc/32)-256))


def main():
    max = MAX31865()
    print("Temperature: ", max.read_temperature())

#if __name__ == '__main__':
#    main()


