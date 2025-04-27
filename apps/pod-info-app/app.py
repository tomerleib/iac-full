from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)

@app.route('/')
def index():
    pod_name = os.environ.get("POD_NAME", "unknown")
    pod_ip = os.environ.get("POD_IP", "unknown")
    return f"POD_NAME: {pod_name}<br>POD_IP: {pod_ip}"

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

