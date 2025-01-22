import board
import time
import busio
import os
import glob
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Initialize I2C and ADS1115
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

# Set the gain for channel 0 (default gain) to 2
ads.gain = 2
channel0 = AnalogIn(ads, ADS.P0)

# Set the gain for channel 1 explicitly to 1
channel1 = AnalogIn(ads, ADS.P1)
channel1.gain = 1

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

# Create or open a file to write data to the SD card
script_dir = os.path.dirname(os.path.realpath(__file__))
log_file = os.path.join(script_dir, "analog_sensor_log.txt")
with open(log_file, 'a') as f:
    while True:
        # Print the analog values and voltage to the console
        print("Analog Value 0: ", channel0.value, "Voltage 0: ", channel0.voltage)
        print("Analog Value 1: ", channel1.value, "Voltage 1: ", channel1.voltage)
        print("Temperature: ", read_temp())

        # Write the same data to the file on the SD card
        f.write("Analog Value 0: {}, Voltage 0: {}\n".format(channel0.value, channel0.voltage))
        f.write("Analog Value 1: {}, Voltage 1: {}\n".format(channel1.value, channel1.voltage))
        temp_c, temp_f = read_temp()
        f.write("Temperature: {:.2f}C, {:.2f}F\n\n".format(temp_c, temp_f))
        
        # Delay for 1 second
        time.sleep(1)
