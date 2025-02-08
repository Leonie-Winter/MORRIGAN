# based on example code at https://github.com/DFRobot/DFRobot_PH/blob/master/python/raspberrypi/DFRobot_PH.py MIT License
# ref Voltage is 3V

import time
"""
measured buffers at 20°C
with temp comp that means the buffers are:
	pH 4.00 and pH 7.02

voltages (in V) measured at each pH are:
	pH 4.00 = 2,049125 = acidV/1000
	pH 7.02 = 1,533125 =  neutralV/1000

"""
acidV      = 2049.12 # in mV
neutralV   = 1533.12 # in mV

def read_PH(voltage):
		'''
		converts voltage to pH with 4 floats
		param voltage = voltage in mV
		return pH_value
        '''
		
		global acidV
		global neutralV
		slope     = (7.02-4.0)/((neutralV-1500.0)/3.0 - (acidV-1500.0)/3.0) 
		intercept = 7.02 - slope*(neutralV-1500.0)/3.0
		pH_value  = slope*((voltage*1000)-1500.0)/3.0+intercept
		if pH_value < 0 or pH_value > 14 :
			print ("read pH above 14 or below 0 \n","it is currently:",pH_value)
			return None
		else:
			return round(pH_value,4)
