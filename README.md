# Wisecow DevOps Assessment

A comprehensive DevOps assessment repository demonstrating containerization, Kubernetes deployment, CI/CD automation, and system monitoring solutions.

## 🎯 Project Overview

**Problem Statement 1 - Wisecow Application (✅ COMPLETE)**
- **Docker containerization** of a bash-based web application
- **Kubernetes deployment** with high availability (3 replicas)
- **CI/CD automation** using GitHub Actions
- **Container registry** integration with Docker Hub
- **TLS/HTTPS security** using Kubernetes Ingress with self-signed certificates
- **Auto-deployment** using Kind cluster in GitHub Actions

**Problem Statement 2 - System Health Monitoring (✅ COMPLETE)**
- **System Health Monitor** (Python) - CPU, memory, disk, process monitoring with alerts
- **Application Health Checker** (Bash) - HTTP status code monitoring for uptime checks
- Both scripts tested and fully functional with comprehensive documentation

**Problem Statement 3 - Additional Solutions (🚧 Optional)**
- KubeArmor zero-trust policy implementation (extra points)

## 📁 Project Structure

```
wisecow-devops-assessment/
├── .github/
│   └── workflows/
│       └── ci-cd.yaml          # GitHub Actions CI/CD pipeline
├── docker/
│   └── Dockerfile              # Container image definition
├── kubernetes/
│   ├── deployment.yaml         # Kubernetes deployment manifest
│   ├── service.yaml            # Kubernetes service manifest
│   └── ingress.yaml            # Kubernetes ingress with TLS
├── problem-2/
│   ├── README.md               # Problem Statement 2 documentation
│   ├── system_health_monitor.py # Python system health monitoring script
│   ├── app_health_checker.sh   # Bash application health checker script
│   ├── system_health.log       # System monitoring logs
│   └── app_health.log          # Application health check logs
├── problem-3/
│   └── README.md                 # Problem Statement 3 (Scripts - TBD)
├── wisecow-app/
│   └── wisecow.sh             # Main application script
└── README.md
```

## 🚀 Features

- **Containerized Application**: Dockerized using Debian slim base image
- **High Availability**: 3 pod replicas for fault tolerance
- **Automated CI/CD**: Automatic Docker image builds on code push
- **Service Exposure**: NodePort service on port 30080
- **Resource Management**: CPU and memory limits configured
- **TLS Security**: HTTPS support with self-signed certificates
- **Auto-Deployment**: Automated deployment to Kind cluster via GitHub Actions

## 🛠️ Technologies Used

- **Docker**: Container runtime
- **Kubernetes**: Container orchestration
- **GitHub Actions**: CI/CD automation
- **Docker Hub**: Container registry
- **Bash**: Application scripting
- **NGINX Ingress**: TLS/HTTPS termination
- **Kind**: Kubernetes in Docker for CI/CD testing

## 📋 Prerequisites

- Docker Desktop or Docker Engine
- Kubernetes cluster (Minikube, Kind, or Docker Desktop K8s)
- kubectl CLI tool
- GitHub account
- Docker Hub account

## 🔧 Local Development

### Build Docker Image

```bash
docker build -t wisecow-app:v1.0 -f docker/Dockerfile .
```

### Run Locally

```bash
docker run -d -p 8080:4499 wisecow-app:v1.0
curl http://localhost:8080
```

## ☸️ Kubernetes Deployment

### Deploy to Kubernetes

```bash
# Apply deployment
kubectl apply -f kubernetes/deployment.yaml

# Apply service
kubectl apply -f kubernetes/service.yaml

# Check pods
kubectl get pods

# Check service
kubectl get service wisecow-service
```

### Access the Application

```bash
# Via NodePort
curl http://localhost:30080

# Via port-forward
kubectl port-forward service/wisecow-service 8080:80
curl http://localhost:8080
```

## 🔒 TLS/HTTPS Setup

### Create Self-Signed Certificates

```bash
# Generate self-signed TLS certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key -out tls.crt \
  -subj "/CN=wisecow.local/O=wisecow"

# Create Kubernetes secret
kubectl create secret tls wisecow-tls \
  --cert=tls.crt \
  --key=tls.key 
  ``` 

### Install NGINX Ingress Controller

```bash
# Install NGINX Ingress
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml

# Wait for ingress to be ready
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

# Apply ingress manifest
kubectl apply -f kubernetes/ingress.yaml
```

### Configure Local DNS
```bash
# Add to /etc/hosts
echo "127.0.0.1 wisecow.local" | sudo tee -a /etc/hosts
```

### Access via HTTPS
```bash
# Test HTTPS access (use -k to ignore self-signed cert warning)
curl -k https://wisecow.local

# Or open in browser: https://wisecow.local (accept security warning)
```

### 🔒 Security Note

**IMPORTANT:** The [tls.crt](cci:7://file:///Users/arpitsg/Desktop/Accuknox-DevOps-Trainee-Practical-Assessment_2025_Arpit/tls.crt:0:0-0:0) and [tls.key](cci:7://file:///Users/arpitsg/Desktop/Accuknox-DevOps-Trainee-Practical-Assessment_2025_Arpit/tls.key:0:0-0:0) files in this repository are **self-signed demo certificates** for local development and testing purposes only.

⚠️ **In production:**
- These files should **NOT** be committed to version control
- Use proper CA-signed certificates from Let's Encrypt, DigiCert, etc.
- Store certificates securely using Kubernetes Secrets or external secret managers (Vault, AWS Secrets Manager)
- The included demo certificates are safe for this assessment environment only


## 🔄 CI/CD Pipeline

The GitHub Actions workflow automatically:

1. **Triggers** on push to `main` branch
2. **Builds** Docker image
3. **Pushes** to Docker Hub as `arpitsh/wisecow:latest`
4. **Tags** with commit SHA for version tracking
5. **Auto-deploys** to Kind Kubernetes cluster for testing

### Pipeline Jobs

- **Job 1: Build and Push** - Builds Docker image and pushes to registry
- **Job 2: Deploy to Kubernetes** - Creates Kind cluster and deploys application

### Setup CI/CD

Add these secrets to your GitHub repository:

- `DOCKERHUB_USERNAME`: Your Docker Hub username
- `DOCKERHUB_TOKEN`: Docker Hub access token

## 📦 Docker Hub

Image available at: [arpitsh/wisecow](https://hub.docker.com/r/arpitsh/wisecow)

```bash
docker pull arpitsh/wisecow:latest
```

## ✅ Testing & Verification

### Test 1: Docker Build and Run

```bash
# Build the image
docker build -t wisecow-test:v1.0 -f docker/Dockerfile .

# Run locally
docker run -d -p 8080:4499 --name wisecow-test wisecow-test:v1.0

# Test
curl http://localhost:8080

# Cleanup
docker stop wisecow-test && docker rm wisecow-test

Expected: ASCII cow with random quote
```

### Test 2: Kubernetes Deployment

```bash
# Check deployment
kubectl get deployment wisecow-deployment

# Check pods
kubectl get pods -l app=wisecow

# Check service
kubectl get service wisecow-service

# View logs
kubectl logs -l app=wisecow

Expected: 3 replicas running, service exposed on port 30080
```

### Test 3: Service Accessibility

```bash
# Test via NodePort
curl http://localhost:30080

# Test via port-forward
kubectl port-forward service/wisecow-service 8081:80
curl http://localhost:8081

Expected: Different quotes from load-balanced pods
```

### Test 4: TLS/HTTPS Verification

```bash
# Verify TLS secret
kubectl get secret wisecow-tls

# Check ingress
kubectl get ingress wisecow-ingress

# Test HTTPS
curl -k https://wisecow.local

# Check TLS version
curl -kv https://wisecow.local 2>&1 | grep "SSL connection"

Expected: HTTPS response with TLSv1.3 encryption
```
### Test 5: CI/CD Pipeline

1. Push changes to `main` branch
2. Check GitHub Actions: [https://github.com/TSM-ArpitSG/wisecow-devops-assessment/actions](https://github.com/TSM-ArpitSG/wisecow-devops-assessment/actions)
3. Verify both jobs complete successfully:
   - Build and Push Docker Image ✅
   - Deploy to Kubernetes ✅

**Expected:** All workflow steps green

## 📊 Resource Configuration

- **Replicas**: 3 pods
- **CPU Request**: 50m
- **CPU Limit**: 100m
- **Memory Request**: 64Mi
- **Memory Limit**: 128Mi

## 🌐 Service Configuration

- **Type**: NodePort
- **Port**: 80 (internal)
- **TargetPort**: 4499 (container)
- **NodePort**: 30080 (external)

## 📝 Application Details

The Wisecow application:
- Runs a bash script that serves HTTP requests
- Uses `fortune` to generate random quotes
- Uses `cowsay` to display ASCII cow art
- Listens on port 4499
- Uses `netcat` as the web server

## 🔐 Security Considerations

- Non-root user in container (Debian default)
- Resource limits to prevent resource exhaustion
- Read-only root filesystem (can be added)
- Network policies (can be implemented)

## 📈 Future Enhancements

- ✅ **TLS/SSL implementation** with Ingress (COMPLETED)
- ✅ **Auto-deployment** with Kind cluster (COMPLETED)
- [ ] Horizontal Pod Autoscaling (HPA)
- [ ] Prometheus metrics integration
- [ ] Health check endpoints
- [ ] Helm chart for deployment
- [ ] KubeArmor security policies

## 👨‍💻 Author

**Arpit Singh**
- GitHub: [@TSM-ArpitSG](https://github.com/TSM-ArpitSG)
- Docker Hub: [arpitsh](https://hub.docker.com/u/arpitsh)

## 📄 License

This project is created for the Accuknox DevOps Trainee Practical Assessment.

## 🙏 Acknowledgments

- Original Wisecow app: [nyrahul/wisecow](https://github.com/nyrahul/wisecow)
- Accuknox for the assessment opportunity

---

**Built with ❤️ for DevOps excellence**
