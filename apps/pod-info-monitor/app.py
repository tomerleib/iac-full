from flask import Flask, jsonify
from kubernetes import client, config
from dataclasses import dataclass
from typing import List, Dict
import os

@dataclass
class PodStatus:
    name: str
    ready: bool
    ip: str

class KubernetesMonitor:
    def __init__(self):
        # Load kubernetes config from environment or default location
        try:
            config.load_incluster_config()
        except config.ConfigException:
            config.load_kube_config()
        
        self.apps_v1 = client.AppsV1Api()
        self.core_v1 = client.CoreV1Api()
        self.namespace = os.getenv('NAMESPACE', 'default')
        self.app_label = os.getenv('APP_LABEL', 'pod-info-app')

    def get_deployment_status(self) -> Dict:
        # Get deployment
        deployment = self.apps_v1.read_namespaced_deployment(
            name=self.app_label,
            namespace=self.namespace
        )
        
        # Get pods
        pods = self.core_v1.list_namespaced_pod(
            namespace=self.namespace,
            label_selector=f"app={self.app_label}"
        )
        
        # Process pod statuses
        pod_statuses = []
        for pod in pods.items:
            ready = False
            for condition in pod.status.conditions:
                if condition.type == 'Ready' and condition.status == 'True':
                    ready = True
                    break
            
            pod_statuses.append(PodStatus(
                name=pod.metadata.name,
                ready=ready,
                ip=pod.status.pod_ip
            ))
        
        return {
            'replicas': deployment.spec.replicas,
            'ready_replicas': deployment.status.ready_replicas,
            'pods': [
                {
                    'name': status.name,
                    'ready': status.ready,
                    'ip': status.ip
                }
                for status in pod_statuses
            ]
        }

app = Flask(__name__)
monitor = KubernetesMonitor()

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/app_status')
def app_status():
    try:
        status = monitor.get_deployment_status()
        return jsonify(status), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)