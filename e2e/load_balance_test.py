import requests
import time
import collections
import argparse
import json
from urllib3.util import Retry
from requests.adapters import HTTPAdapter

def main():
    parser = argparse.ArgumentParser(description='Test load balancing for pod-info-app service')
    parser.add_argument('--url', default='http://localhost', help='URL of the pod-info-app service')
    parser.add_argument('--requests', type=int, default=20, help='Number of requests to make')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests in seconds')
    args = parser.parse_args()

    pod_counts = collections.Counter()
    total_requests = args.requests

    print(f"Making {total_requests} requests to {args.url} with new connections for each request...")
    print(f"Delay between requests: {args.delay} seconds")
    print("-" * 60)

    for i in range(total_requests):
        # Create a new session for each request to disable connection pooling
        session = requests.Session()
        
        # Explicitly close connections after each request
        session.headers.update({'Connection': 'close'})
        
        # Disable keep-alive
        adapter = HTTPAdapter(
            max_retries=Retry(
                total=3,
                backoff_factor=0.5
            )
        )
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        try:
            response = session.get(args.url, timeout=5)
            
            # Parse the JSON response
            try:
                data = response.json()
                
                # Extract pod information from the JSON response
                pod_name = None
                pod_ip = None
                
                if 'pod' in data:
                    pod_info = data['pod']
                    pod_name = pod_info.get('name')
                    pod_ip = pod_info.get('ip')
                
                if pod_name:
                    pod_counts[pod_name] += 1
                    print(f"Request {i+1}: Hit pod {pod_name} (IP: {pod_ip})")
                else:
                    print(f"Request {i+1}: Unable to determine pod (Response: {response.text[:50]}...)")
            
            except json.JSONDecodeError:
                # Fallback to the old parsing method if JSON parsing fails
                content = response.text
                pod_name = None
                pod_ip = None
                
                for line in content.split('<br>'):
                    if 'POD_NAME:' in line:
                        pod_name = line.split('POD_NAME:')[1].strip()
                    elif 'POD_IP:' in line:
                        pod_ip = line.split('POD_IP:')[1].strip()
                
                if pod_name:
                    pod_counts[pod_name] += 1
                    print(f"Request {i+1}: Hit pod {pod_name} (IP: {pod_ip})")
                else:
                    print(f"Request {i+1}: Unable to determine pod (Response: {content[:50]}...)")
        
        except requests.exceptions.RequestException as e:
            print(f"Request {i+1}: Error - {e}")
        
        # Always close the session
        session.close()
        
        # Add delay between requests
        if i < total_requests - 1:
            time.sleep(args.delay)
    
    print("-" * 60)
    print("Request distribution:")
    for pod, count in pod_counts.items():
        percentage = (count / total_requests) * 100
        print(f"  {pod}: {count} requests ({percentage:.1f}%)")

    if len(pod_counts) > 1:
        print("\nLoad balancing appears to be working! Requests were distributed across multiple pods.")
    elif len(pod_counts) == 1:
        print("\nLoad balancing does not appear to be working. All requests went to the same pod.")
    else:
        print("\nNo valid responses from pods were received.")

if __name__ == "__main__":
    main()

