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
        # Get the current time for the timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Get the analog values and temperature
        analog_value_0 = channel0.value
        voltage_0 = channel0.voltage
        analog_value_1 = channel1.value
        voltage_1 = channel1.voltage
        temp_c, temp_f = read_temp()

        # Print the analog values and voltage to the console with timestamp
        print(f"[{current_time}] Analog Value 0: {analog_value_0}, Voltage 0: {voltage_0}")
        print(f"[{current_time}] Analog Value 1 (scaled): {analog_value_1}, Voltage 1 (scaled): {voltage_1}")
        print(f"[{current_time}] Temperature: {temp_c:.2f}C, {temp_f:.2f}F")

        # Write the measurement to the log file with timestamp
        f.write(f"[{current_time}] Analog Value 0: {analog_value_0}, Voltage 0: {voltage_0}\n")
        f.write(f"[{current_time}] Analog Value 1: {analog_value_1}, Voltage 1: {voltage_1}\n")
        f.write(f"[{current_time}] Temperature: {temp_c:.2f}C, {temp_f:.2f}F\n\n")
        
        # Delay for 1 second
        time.sleep(1)
