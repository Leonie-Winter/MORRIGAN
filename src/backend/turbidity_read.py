
# -1,44010724307339 * x + 2865,54817556838
# R^2 = 0,968250044060315

def read_turbidity(voltage):
    turbidity_value = -1458.23351684657 * voltage + 3011.70589885467
    return round(turbidity_value)
