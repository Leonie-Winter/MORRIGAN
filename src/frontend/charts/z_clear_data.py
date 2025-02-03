import json

# Path to your JSON file
file_path = "data.json"

# Overwrite the file with an empty array
with open(file_path, "w") as file:
    json.dump([], file)
