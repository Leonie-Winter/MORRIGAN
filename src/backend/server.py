from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__, static_folder="static")
CORS(app, resources={r"/run-script": {"origins": "*"}})

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "main.py")

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route('/run-script', methods=['GET'])
def run_script():
    try:
        result = subprocess.run(f"python3 {SCRIPT_PATH}", capture_output=True, text=True, shell=True)
        return jsonify({"output": result.stdout.strip(), "error": result.stderr.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
