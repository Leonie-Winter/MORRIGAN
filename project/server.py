from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__, static_folder="static")
CORS(app)

# Serve the frontend
@app.route('/')
def serve_index():
    return send_from_directory("static", "index.html")

# Run the Python script when the button is pressed
@app.route('/run-script', methods=['GET'])
def run_script():
    try:
        # Adjust command for Windows
        result = subprocess.run(["python", "somefile.py"], capture_output=True, text=True, shell=True)
        return jsonify({"output": result.stdout, "error": result.stderr})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
