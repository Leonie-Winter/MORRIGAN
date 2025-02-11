def read_DO(voltage, temperature):
    voltage_comped = voltage - (0.04666 * (temperature - 21.5))
    c_O2 = (voltage_comped - 0.036) / 0.01829
    
    return c_O2
