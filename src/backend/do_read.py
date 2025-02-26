def read_DO(voltage, temperature):
    '''
    calculated the DO value
    param: voltage (float): measured voltage from the DO sensor
    param: temperature (float): measured temperature from the temperature sensor
    return: DO (float): dissolved oxygen concentration in mg/L
    '''
    voltage_comped = voltage - (0.04666 * (temperature - 21.5))
    c_O2 = (voltage_comped - 0.036) / 0.01829

    return c_O2
