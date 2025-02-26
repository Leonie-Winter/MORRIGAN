from ph_read import *
from temp_read import *
from do_read import *
from tds_read import *
from turbidity_read import *
import board
import time
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import os
import json
import sqlite3
from datetime import datetime

# Initialize I2C and ADS1115
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c, 0x08)

# Database setup
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database"))
DB_PATH = os.path.join(BASE_DIR, "sensor_data.db")

def init_db():
    """Initialize the database and create table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            sensor TEXT,
            value REAL,
            voltage REAL,
            elapsed_seconds INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()  # init database

# Define sensor switching function
def switch_sensor(sensor):
    return AnalogIn(ads, {"ph": ADS.P3, "TDS": ADS.P0, "turbidity": ADS.P1, "DO": ADS.P2}.get(sensor, ADS.P3))


# Initialize log variables
start_time = None 
log = []

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_FILE_PATH = os.path.join(BASE_DIR, "frontend", "charts", "data.json")

def log_data(sensor, value, voltage):
    ts, elapsed = datetime.now().isoformat(), int(time.time() - start_time)
    data = {"seconds": elapsed, "timestamp": ts, "voltage": voltage, sensor: value}
    json.dump(data, open(DATA_FILE_PATH, "w"), indent=4)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO sensor_logs VALUES (NULL, ?, ?, ?, ?, ?)", tuple(data.values()))

while True:
    temp = read_temp()
    log_data("temperature", temp, voltage=None)  
    
    ph_channel = switch_sensor("ph")
    ph_voltage = ph_channel.voltage
    ph_value = read_PH(ph_voltage)
    log_data("PH", ph_value, ph_voltage)
    time.sleep(1)

    TDS_channel = switch_sensor("TDS")
    TDS_voltage = TDS_channel.voltage
    EC_value = read_EC(TDS_voltage, temp)
    log_data("EC", EC_value, TDS_voltage)  
    TDS_value = read_tds(EC_value)
    log_data("TDS", TDS_value, TDS_voltage)
    time.sleep(1)

    turbidity_channel = switch_sensor("turbidity")
    turbidity_voltage = turbidity_channel.voltage
    turbidity_value = read_turbidity(turbidity_voltage)
    log_data("turbidity", turbidity_value, turbidity_voltage)
    time.sleep(1)

    DO_channel = switch_sensor("DO")
    DO_voltage = DO_channel.voltage
    DO_value = read_DO(DO_voltage,temp)
    log_data("DO", DO_value, DO_voltage)
    time.sleep(1)
