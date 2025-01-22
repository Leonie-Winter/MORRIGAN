import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Set up I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Set the correct address (0x08 if detected)
ads = ADS.ADS1115(i2c, 0x08)  # Or 0x48 if that's the correct address
ads.gain = 1
# Set up analog input channel
chan = AnalogIn(ads, ADS.P3)

# Read and print value
while True:
	print(f"Analog value: {chan.value}")
	print(f"Voltage: {chan.voltage}V")
