from flask import Flask, jsonify
import os
import socket
import datetime

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/')
def pod_info():
    pod_name = os.environ.get("POD_NAME", "unknown")
    pod_ip = os.environ.get("POD_IP", "unknown")
    hostname = socket.gethostname()
    timestamp = datetime.datetime.now().isoformat()
    
    return jsonify({
        "pod": {
            "name": pod_name,
            "ip": pod_ip,
            "hostname": hostname
        },
        "timestamp": timestamp,
        "status": "running"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)