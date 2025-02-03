import json
import random
import time

def append_randomized_data(filepath):
    # Initialize the time step
    time_step = 16.67

    # Define ranges for different parameters
    temperature_range = (10, 40)  # Celsius
    ph_range = (6.5, 8.5)         # pH units
    tds_range = (100, 500)        # Total Dissolved Solids in ppm
    do_range = (5, 14)            # Dissolved Oxygen in mg/L
    turbidity_range = (0.5, 5)    # Turbidity in NTU

    while True:
        # Read the existing data if the file exists
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        # Determine the next milliseconds value
        if data:
            last_milliseconds = data[-1]["milliseconds"]
        else:
            last_milliseconds = 0

        milliseconds = round(last_milliseconds + time_step, 2)
        sensor_type = random.choice(["temperature", "PH", "TDS", "DO", "turbidity"])

        if sensor_type == "temperature":
            value = round(random.uniform(*temperature_range), 2)
        elif sensor_type == "PH":
            value = round(random.uniform(*ph_range), 2)
        elif sensor_type == "TDS":
            value = round(random.uniform(*tds_range), 2)
        elif sensor_type == "DO":
            value = round(random.uniform(*do_range), 2)
        elif sensor_type == "turbidity":
            value = round(random.uniform(*turbidity_range), 2)

        data.append({"milliseconds": milliseconds, sensor_type: value})

        # Write the updated data back to the JSON file
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Added new data point: {{'milliseconds': {milliseconds}, '{sensor_type}': {value}}}")

        # Wait for some time before adding the next data point
        time.sleep(1/60)  # Adjust the delay as needed

# Filepath for the output JSON file
output_file = "data.json"

# Continuously append data to the file
append_randomized_data(output_file)
