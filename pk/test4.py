import board
import time
import busio
import os
import glob
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from datetime import datetime

# Initialize I2C and ADS1115
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

# Set the gain for the entire ADS1115 device (channel 0 gain will be 2)
ads.gain = 2
channel0 = AnalogIn(ads, ADS.P0)

# For channel 1, we will manually adjust the readings to simulate a gain of 1
channel1 = AnalogIn(ads, ADS.P1)

# Setup for reading temperature from a 1-Wire device (e.g., DS18B20)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

# Get the current directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

# Generate a timestamp for the log file name (format: YYYY-MM-DD_HH-MM-SS)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = os.path.join(script_dir, f"analog_sensor_log_{timestamp}.txt")

# Create or open a file to write data with timestamped filename
with open(log_file, 'a') as f:
    while True:
        # Print the analog values and voltage to the console
        print("Analog Value 0: ", channel0.value, "Voltage 0: ", channel0.voltage)
        print("Analog Value 1 (scaled): ", channel1.value, "Voltage 1 (scaled): ", channel1.voltage)

        # Manually scale the value for channel 1 to simulate a gain of 1
        # Scaling factor for channel 1: Adjust the raw value to account for gain
        scaled_channel1_value = (channel1.value / 32768.0) * 32768.0  # Normalize to 16-bit range

        # Print the adjusted value for channel 1
        print("Scaled Analog Value 1 (Gain 1): ", scaled_channel1_value)

        # Write the same data to the file with timestamped filename
        f.write("Analog Value 0: {}, Voltage 0: {}\n".format(channel0.value, channel0.voltage))
        f.write("Scaled Analog Value 1: {}, Voltage 1: {}\n".format(scaled_channel1_value, channel1.voltage))
        temp_c, temp_f = read_temp()
        f.write("Temperature: {:.2f}C, {:.2f}F\n\n".format(temp_c, temp_f))
        
        # Delay for 1 second
        time.sleep(1)
