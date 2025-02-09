import json
import random
import os.path as os_path

def generate_randomized_data(filepath, num_entries=50):
    # Initialize the time step
    time_step = 16.67
    
    # Define ranges for different parameters
    temperature_range = (10, 40)  # Celsius
    ph_range = (6.5, 8.5)         # pH units
    tds_range = (100, 500)        # Total Dissolved Solids in ppm
    do_range = (5, 14)            # Dissolved Oxygen in mg/L
    turbidity_range = (0.5, 5)    # Turbidity in NTU
    ec_range = (50, 2000) 

    # List to hold the randomized data
    data = []

    for i in range(num_entries):
        seconds = round(i * time_step, 2)
        sensor_type = random.choice(["temperature", "PH", "TDS", "DO", "turbidity", "EC"])

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
        elif sensor_type == "EC":  # Added EC data generation
            value = round(random.uniform(*ec_range), 2)

        data.append({"seconds": seconds, sensor_type: value})

    # Write the randomized data to the JSON file
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Randomized data written to {filepath}")

# Filepath for the output JSON file
output_file = "data.json"
file_location = os_path.join(os_path.dirname(os_path.abspath(__file__)), output_file)

# Generate and save the data
generate_randomized_data(file_location)
