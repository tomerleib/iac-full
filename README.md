# Multi-App Kubernetes Terraform Infrastructure

This repository contains Infrastructure as Code (IaC) for deploying multiple applications on Kubernetes using Terraform. The infrastructure is designed to be modular, reusable, and follows infrastructure-as-code best practices.

## Project Structure

```
.
├── apps/                    # Application manifests and configurations
│   ├── pod-info-app/       # Pod Info Application
│   └── pod-info-monitor/   # Pod Info Monitor Application
├── terraform/              # Terraform configurations
│   ├── live/              # Environment-specific configurations
│   └── modules/           # Reusable Terraform modules
└── .github/               # GitHub Actions workflows
```

## Prerequisites

Before you begin, ensure you have the following tools installed:

- [Terraform](https://www.terraform.io/downloads.html) (v1.0.0 or later)
- [kubectl](https://kubernetes.io/docs/tasks/tools/) (v1.20.0 or later)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/) or [k3d](https://k3d.io/) for local Kubernetes development

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/multi-app-k8s-terraform.git
   cd multi-app-k8s-terraform
   ```

2. **Initialize Terraform**
   ```bash
   cd terraform/live/dev  # or your target environment
   terraform init
   ```

3. **Start local Kubernetes cluster** (if using Minikube)
   ```bash
   minikube start
   ```

4. **Apply Terraform configuration**
   ```bash
   terraform plan
   terraform apply
   ```

5. **Verify the deployment**
   ```bash
   kubectl get pods
   kubectl get services
   ```

## Accessing the Applications

After deploying the infrastructure, you can access the applications through their respective URLs:

1. **Pod Info App**
   ```bash
   # If using Minikube
   minikube service pod-info-app --url
   
   # If using k3d
   kubectl get svc pod-info-app -o jsonpath='{.status.loadBalancer.ingress[0].ip}:{.spec.ports[0].port}'
   ```

2. **Pod Info Monitor**
   ```bash
   # If using Minikube
   minikube service pod-info-monitor --url
   
   # If using k3d
   kubectl get svc pod-info-monitor -o jsonpath='{.status.loadBalancer.ingress[0].ip}:{.spec.ports[0].port}'
   ```

## Testing Load Balancing

To verify that the load balancing is working correctly, you can use the provided load balancing test script:

1. **Install Python dependencies**
   ```bash
   pip install requests
   ```

2. **Run the load balancing test**
   ```bash
   # Navigate to the e2e directory
   cd terraform/live/e2e
   
   # Run the test with default settings (20 requests)
   python load_balance_test.py --url http://<your-service-url>
   
   # Or customize the test parameters
   python load_balance_test.py --url http://<your-service-url> --requests 50 --delay 0.5
   ```

The script will:
- Make multiple requests to the service
- Track which pods handle each request
- Display the distribution of requests across pods
- Verify if load balancing is working correctly

Example output:
```
Making 20 requests to http://localhost:8081 with new connections for each request...
Delay between requests: 1.0 seconds
------------------------------------------------------------
Request 1: Hit pod pod-info-app-5d4f8b9c76-abc12 (IP: 10.0.0.1)
Request 2: Hit pod pod-info-app-5d4f8b9c76-def34 (IP: 10.0.0.2)
...
------------------------------------------------------------
Request distribution:
  pod-info-app-5d4f8b9c76-abc12: 10 requests (50.0%)
  pod-info-app-5d4f8b9c76-def34: 10 requests (50.0%)

Load balancing appears to be working! Requests were distributed across multiple pods.
```

## Infrastructure Components

The infrastructure includes:

- Kubernetes cluster configuration
- Application deployments
- Service configurations
- Monitoring setup
- Network policies
- Resource quotas and limits

## Development Workflow

1. Make changes to the Terraform configurations in the appropriate module
2. Run `terraform fmt` to format the code
3. Run `terraform validate` to check for errors
4. Create a pull request with your changes
5. The CI/CD pipeline will automatically validate and apply the changes

