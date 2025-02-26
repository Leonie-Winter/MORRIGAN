# reference voltage is 2.3V
"""
voltages (in V) measured at each EC (in µ/cm) are:
    0,066625 V = 48   µ/cm
    0,13325  V = 101  µ/cm
    0,256125 V = 186  µ/cm
    0,339625 V = 277  µ/cm
    0,470125 V = 375  µ/cm
    0,54775  V = 440  µ/cm
    1,594875 V = 1400 µ/cm 

that gives a line with the function
890,419135176094 * x - 29,6974742651173
where x is the voltage in V

this line has a coefficient of determination of 
R^2 = 0,999009283277105
"""

def read_EC(voltage, temperature):
    '''
		converts voltage in V to EC in mikrosiemens/cm with no floats with temperature compensation
		param voltage = voltage in V
        param temperature = temperature in °C
		return EC_value
    '''
    EC_value = (890.419135176094 * voltage + 29.6974742651173) * (1.0 + 0.02 * (temperature - 25))
    return round(EC_value)

def read_tds(EC_value):
    '''
        converts EC in mikrosiemens to TDS in ppm
        param EC_value = EC in mikrosiemens/cm
        return TDS_value
    '''
    TDS_value = EC_value * 0.64 #0.64 is a good average for k, k might be higher or lower depending on the specific type of water
    return round(TDS_value)
