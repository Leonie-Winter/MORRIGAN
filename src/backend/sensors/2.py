import time
import board
import busio
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

class GravityTDS:
    def __init__(self, adc_channel):
        self.adc_channel = adc_channel
        self.aref = 3.3  # Default reference voltage for Raspberry Pi
        self.adc_range = 32768  # ADS1115 is a 16-bit ADC
        self.temperature = 25.0
        self.calibration_factor = 2.0  # Default calibration factor; adjust during calibration

    def set_temperature(self, temperature):
        self.temperature = temperature

    def update(self):
        self.raw_value = self.adc_channel.value

    def get_tds_value(self):
        # Convert raw ADC value to voltage
        voltage = (self.raw_value / self.adc_range) * self.aref
        # Apply temperature compensation
        temperature_coefficient = 1 + 0.02 * (self.temperature - 25)
        # Calculate TDS value
        tds_value = (voltage * 1000) / (self.calibration_factor * temperature_coefficient)
        return tds_value, voltage

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize ADS1115
ads = ADS1115(i2c)

# Configure the ADC channel (e.g., A1)
channel = AnalogIn(ads, 1)

tds_sensor = GravityTDS(channel)

def main():
    while True:
        tds_sensor.set_temperature(25)  # Update temperature if needed
        tds_sensor.update()  # Read ADC value

        # Get TDS and voltage
        tds_value, voltage = tds_sensor.get_tds_value()

        # Debug: Output readings
        print(f"Raw ADC Value: {tds_sensor.raw_value}")
        print(f"Voltage: {voltage:.3f} V")
        print(f"TDS Value: {tds_value:.0f} ppm")

        time.sleep(1)

if __name__ == "__main__":
    main()
1~import time
import board
import busio
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

class GravityTDS:
    def __init__(self, adc_channel):
        self.adc_channel = adc_channel
        self.aref = 3.3  # Default reference voltage for Raspberry Pi
        self.adc_range = 32768  # ADS1115 is a 16-bit ADC
        self.temperature = 25.0
        self.calibration_factor = 2.0  # Default calibration factor; adjust during calibration

    def set_temperature(self, temperature):
        self.temperature = temperature

    def update(self):
        self.raw_value = self.adc_channel.value

    def get_tds_value(self):
        # Convert raw ADC value to voltage
        voltage = (self.raw_value / self.adc_range) * self.aref
        # Apply temperature compensation
        temperature_coefficient = 1 + 0.02 * (self.temperature - 25)
        # Calculate TDS value
        tds_value = (voltage * 1000) / (self.calibration_factor * temperature_coefficient)
        return tds_value, voltage

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize ADS1115
ads = ADS1115(i2c)

# Configure the ADC channel (e.g., A1)
channel = AnalogIn(ads, 1)

tds_sensor = GravityTDS(channel)

def main():
    while True:
        tds_sensor.set_temperature(25)  # Update temperature if needed
        tds_sensor.update()  # Read ADC value

        # Get TDS and voltage
        tds_value, voltage = tds_sensor.get_tds_value()

        # Debug: Output readings
        print(f"Raw ADC Value: {tds_sensor.raw_value}")
        print(f"Voltage: {voltage:.3f} V")
        print(f"TDS Value: {tds_value:.0f} ppm")

        time.sleep(1)

if __name__ == "__main__":
    main()
