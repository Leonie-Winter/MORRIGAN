# based on https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/Raspberry_Pi_DS18B20_Temperature_Sensing/code.py MIT license

import os
import glob
import time

# init kernel modules for w1
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
# set directory that the temp sensor uses
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    # read the raw txt file the temp sensor writes to
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    # cut the verification line and convert raw reading to °C
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return round(temp_c,2)
