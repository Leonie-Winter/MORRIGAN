import time
import Adafruit_ADS1x15
adc = Adafruit_ADS1x15.ADS1115() # Create an ADS1115 ADC (16-bit) instance
GAIN = 1
print('[press ctrl+c to end the script]')
try: # Main program loop
	while True:
		values = adc.read_adc(3, gain=GAIN) # Read the ADC channel 0 value
		print('{0:>6}'.format(values))
		time.sleep(0.5)
# Scavenging work after the end of the program
except KeyboardInterrupt:
	print('Script end!')
