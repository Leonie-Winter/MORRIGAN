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
DB_PATH = os.path.join(os.path.dirname(__file__), "sensor_data.db")

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

init_db()  # Ensure the database is ready

# Define sensor switching function
def switch_sensor(sensor):
    if sensor == "ph":
        ads.gain = 1
        chan = AnalogIn(ads, ADS.P3)
    elif sensor == "TDS": 
        ads.gain = 1
        chan = AnalogIn(ads, ADS.P0)
    elif sensor == "turbidity": 
        ads.gain = 1
        chan = AnalogIn(ads, ADS.P1)
    elif sensor == "DO":
        ads.gain = 1
        chan = AnalogIn(ads, ADS.P2)
    else: 
        raise ValueError("Invalid sensor type passed to switch_sensor")
    
    return chan

# Initialize log variables
start_time = None 
log = []

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_FILE_PATH = os.path.join(BASE_DIR, "frontend", "charts", "data.json")

def log_data(sensor, value, voltage):
    global start_time
    
    if start_time is None:
        start_time = time.time()
    
    elapsed_seconds = int(time.time() - start_time)
    timestamp = datetime.now().isoformat()  
    
    sensor_data = {
        "seconds": elapsed_seconds, 
        "timestamp": timestamp,
        "voltage": voltage,
        sensor: value  
    }
    
    log.append(sensor_data)

    # Save to JSON
    os.makedirs(os.path.dirname(DATA_FILE_PATH), exist_ok=True)
    with open(DATA_FILE_PATH, "w") as f:
        json.dump(log, f, indent=4)

    # Save to SQLite Database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sensor_logs (timestamp, sensor, value, voltage, elapsed_seconds)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, sensor, value, voltage, elapsed_seconds))
    conn.commit()
    conn.close()

while True:
    temp = read_temp()
    log_data("temperature", temp, voltage=None)  
    
    ph_channel = switch_sensor("ph")
    ph_voltage = ph_channel.voltage
    ph_value = read_PH(ph_voltage)
    log_data("PH", ph_value, ph_voltage)
    time.sleep(15 / 60)

    TDS_channel = switch_sensor("TDS")
    TDS_voltage = TDS_channel.voltage
    EC_value = read_EC(TDS_voltage, temp)
    log_data("EC", EC_value, TDS_voltage)  
    TDS_value = read_tds(EC_value)
    log_data("TDS", TDS_value, TDS_voltage)
    time.sleep(15 / 60)

    turbidity_channel = switch_sensor("turbidity")
    turbidity_voltage = turbidity_channel.voltage
    turbidity_value = read_turbidity(turbidity_voltage)
    log_data("turbidity", turbidity_value, turbidity_voltage)
    time.sleep(15 / 60)

    DO_channel = switch_sensor("DO")
    DO_voltage = DO_channel.voltage
    DO_value = read_DO(DO_voltage,temp)
    log_data("DO", DO_value, DO_voltage)
    time.sleep(15 / 60)
