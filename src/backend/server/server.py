from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__, static_folder="static")
CORS(app)

# Get the full absolute path to somefile.py
SCRIPT_PATH = os.path.abspath("somefile.py")

@app.route('/')
def serve_index():
    return send_from_directory("static", "index.html")

@app.route('/run-script', methods=['GET'])
def run_script():
    try:
        # Run somefile.py
        result = subprocess.run(["python", SCRIPT_PATH], capture_output=True, text=True, shell=True)
        return jsonify({"output": result.stdout, "error": result.stderr})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
