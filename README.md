# Wisecow DevOps Assessment

A containerized and Kubernetes-deployed application that serves random wisdom quotes with ASCII cow art.

## 🎯 Project Overview

This project demonstrates:
- **Docker containerization** of a bash-based web application
- **Kubernetes deployment** with high availability (3 replicas)
- **CI/CD automation** using GitHub Actions
- **Container registry** integration with Docker Hub

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
│   └── service.yaml            # Kubernetes service manifest
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

## 🛠️ Technologies Used

- **Docker**: Container runtime
- **Kubernetes**: Container orchestration
- **GitHub Actions**: CI/CD automation
- **Docker Hub**: Container registry
- **Bash**: Application scripting

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

## 🔄 CI/CD Pipeline

The GitHub Actions workflow automatically:

1. **Triggers** on push to `main` branch
2. **Builds** Docker image
3. **Pushes** to Docker Hub as `arpitsh/wisecow:latest`
4. **Tags** with commit SHA for version tracking

### Setup CI/CD

Add these secrets to your GitHub repository:

- `DOCKERHUB_USERNAME`: Your Docker Hub username
- `DOCKERHUB_TOKEN`: Docker Hub access token

## 📦 Docker Hub

Image available at: [arpitsh/wisecow](https://hub.docker.com/r/arpitsh/wisecow)

```bash
docker pull arpitsh/wisecow:latest
```

## 🧪 Testing

### Test Application Response

```bash
# Should return a cow with a random quote
curl http://localhost:30080
```

### Verify Kubernetes Resources

```bash
# Check deployment
kubectl get deployment wisecow-deployment

# Check pods
kubectl get pods -l app=wisecow

# Check service
kubectl get service wisecow-service

# View logs
kubectl logs -l app=wisecow
```

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

- [ ] TLS/SSL implementation with Ingress
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
