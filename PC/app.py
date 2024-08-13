from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import re

app = Flask(__name__)
CORS(app) 


@app.route('/')
def index():
    return "Welcome to the Face Authentication System!"


@app.route('/request-access', methods=['POST'])
def request_access():
    try:
        
        result = subprocess.run(['python', 'server_script.py'], capture_output=True, text=True)

        
        print("Result stdout:", result.stdout)
        print("Result stderr:", result.stderr)
        print("Return code:", result.returncode)

        if result.returncode == 0:
            
            match = re.search(r"Server Response: (.*), Authenticated", result.stdout)
            if match:
                name = match.group(1)
                return jsonify(message=f"Hi {name}, you are authenticated!"), 200
            else:
                return jsonify(message="Authentication failed. No valid response."), 500
        else:
            return jsonify(message="Error executing script!", error=result.stderr.strip()), 500
    except Exception as e:
        return jsonify(message=f"Error: {str(e)}"), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
