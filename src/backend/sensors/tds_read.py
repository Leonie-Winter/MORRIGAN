# 806,855840052007 * Voltage  + 56,318844093962
from main import *

def read_EC(voltage):
    global temperature
    EC_Vlaue = (805.855840052007 * voltage + 56.318844093962) * (1.0 + 0.02 * (temperature - 25))
    return EC_value

def read_tds(EC_value):
    TDS_value = EC_value * 0.64
    return round(TDS_value)
