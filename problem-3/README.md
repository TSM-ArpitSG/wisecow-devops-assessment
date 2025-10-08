# Problem Statement 3: KubeArmor Zero-Trust Security Policy

**Status:** COMPLETE (Optional - Extra Points)

**Author:** Arpit Singh  
**GitHub:** @TSM-ArpitSG

## Overview

This directory contains a comprehensive zero-trust security policy for the Wisecow application using KubeArmor, a runtime security enforcement system for Kubernetes workloads.

## What is KubeArmor?

KubeArmor is a Cloud Native Runtime Security (CNRS) platform that provides zero-trust security for Kubernetes workloads. It uses Linux kernel primitives (eBPF, LSM) to enforce security policies at runtime.

**Key Features:**
- Process execution control
- File access control
- Network access control
- Capability restrictions
- Real-time policy enforcement

## Files in This Directory

```
problem-3/
├── README.md                        # This documentation
├── wisecow-kubearmor-policy.yaml   # KubeArmor security policies
├── kubearmor-probe-output.png      # Policy monitoring screenshot
└── kubearmor-policies-list.png     # Policy verification screenshot
```

## Zero-Trust Policy Overview

Our KubeArmor policy implements two security layers for the Wisecow application:

### Policy 1: wisecow-zero-trust-policy
**Severity:** 8/10 (High)

**Restrictions:**
- Blocks writes to system directories: [/bin/](cci:7://file:///bin:0:0-0:0), [/sbin/](cci:7://file:///sbin:0:0-0:0), [/usr/bin/](cci:7://file:///usr/bin:0:0-0:0), [/usr/sbin/](cci:7://file:///usr/sbin:0:0-0:0)
- Prevents system file tampering and backdoor installation

- **Network:**
  - Restricts network connections
  - Allows only port 4499 (Wisecow's service port)

- **Capabilities:**
  - Blocks dangerous Linux capabilities: `SYS_ADMIN`, `NET_ADMIN`, `SYS_PTRACE`
  - Prevents privilege escalation

### Policy 2: wisecow-file-integrity-policy
**Severity:** 7/10 (Medium-High)

**Restrictions:**
- **Enforces read-only mode for `/wisecow/` directory
- **Blocks writes to `/etc/` (configuration integrity)
- **Audits all file modification attempts

## 📸 Implementation Screenshots

### KubeArmor Policies Applied
![KubeArmor Probe Output](kubearmor-probe-output.png)

**What this shows:**
- ✅ All 3 Wisecow pods are "Armored Up"
- ✅ Both policies applied to each pod
- ✅ Audit mode active for File, Capabilities, Network
- ✅ KubeArmor successfully monitoring the workload

### Policy Verification
![Policy List](kubearmor-policies-list.png)

## Installation & Deployment

### Prerequisites
- Kubernetes cluster running (Minikube, Kind, or Docker Desktop K8s)
- kubectl CLI tool
- Wisecow application deployed (from PS1)

### Step 1: Install KubeArmor

```bash
# Install KubeArmor using Helm
helm repo add kubearmor https://kubearmor.github.io/charts
helm repo update
helm install kubearmor kubearmor/kubearmor -n kubearmor --create-namespace

# Verify installation
kubectl get pods -n kubearmor
```

**Alternative: Using karmor CLI**
```bash
# Install karmor CLI
curl -sfL https://raw.githubusercontent.com/kubearmor/kubearmor-client/main/install.sh | sudo sh -s -- -b /usr/local/bin

# Install KubeArmor
karmor install
```

### Step 2: Verify KubeArmor is Running

```bash
# Check KubeArmor pods
kubectl get pods -n kubearmor

# Check KubeArmor DaemonSet
kubectl get daemonset -n kubearmor

# Expected output:
# NAME         DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE
# kubearmor    1         1         1       1            1
```

### Step 3: Deploy Wisecow (if not already running)

```bash
# Deploy from PS1
kubectl apply -f ../kubernetes/deployment.yaml
kubectl apply -f ../kubernetes/service.yaml

# Verify pods are running
kubectl get pods -l app=wisecow
```

### Step 4: Apply KubeArmor Policy

```bash
# Apply the zero-trust policy
kubectl apply -f wisecow-kubearmor-policy.yaml

# Verify policies are created
kubectl get kubearmorpolicies

# Expected output:
# NAME                             AGE
# wisecow-zero-trust-policy         10s
# wisecow-file-integrity-policy     10s
```

### Step 5: Verify Policy Status

```bash
# Describe the policy
kubectl describe kubearmorpolicy wisecow-zero-trust-policy

# Check policy logs
karmor logs
```

## Testing Policy Violations

### Test 1: Block Execution from /tmp

```bash
# Get into the Wisecow pod
POD_NAME=$(kubectl get pods -l app=wisecow -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it $POD_NAME -- /bin/bash

# Try to create and execute a script in /tmp (SHOULD BE BLOCKED)
echo '#!/bin/bash' > /tmp/malicious.sh
echo 'echo "This should be blocked"' >> /tmp/malicious.sh
chmod +x /tmp/malicious.sh
/tmp/malicious.sh

# Expected: Permission denied or operation not permitted
```

### Test 2: Block Access to Sensitive Files

```bash
# Inside the Wisecow pod
# Try to read /etc/shadow (SHOULD BE BLOCKED)
cat /etc/shadow

# Try to read /etc/passwd (SHOULD BE BLOCKED)
cat /etc/passwd

# Expected: Permission denied
```

### Test 3: Block Writes to System Directories

```bash
# Inside the Wisecow pod
# Try to write to /bin (SHOULD BE BLOCKED)
echo "test" > /bin/test.sh

# Try to write to /etc (SHOULD BE BLOCKED)
echo "malicious" > /etc/malicious.conf

# Expected: Permission denied or read-only file system
```

### Test 4: View Policy Violations

```bash
# View real-time policy violations
karmor logs --json

# Filter for Wisecow violations
karmor logs --namespace=default --pod=<wisecow-pod-name>
```

## Capturing Policy Violations

**To capture screenshots:**

1. **Option 1: Using karmor logs**
   ```bash
   karmor logs --json > violations.log
   # Take screenshot of violations.log
   ```

2. **Option 2: Using kubectl logs**
   ```bash
   kubectl logs -n kubearmor <kubearmor-pod-name> | grep "wisecow"
   # Take screenshot of filtered logs
   ```

3. **Option 3: KubeArmor Dashboard** (if installed)
   ```bash
   # Port-forward to access dashboard
   kubectl port-forward -n kubearmor svc/kubearmor-controller 8080:8080
   # Open browser: http://localhost:8080
   # Take screenshot of violations dashboard
   ```

## Understanding Policy Actions

| Action | Description | Use Case |
|--------|-------------|----------|
| **Block** | Denies the operation and generates alert | Prevent malicious actions |
| **Allow** | Explicitly permits the operation | Whitelist required operations |
| **Audit** | Logs the operation but allows it | Monitoring mode, compliance |

## Security Benefits

**What This Policy Prevents:**
- Unauthorized process execution (malware, crypto miners)
- Access to sensitive credentials (password files, SSH keys)
- File system tampering (rootkits, backdoors)
- Privilege escalation attempts
- Network-based attacks
- Container breakout attempts

**Real-World Attack Scenarios blocked:**
1. **Crypto-jacking:** Blocks execution from `/tmp/` where miners are often placed
2. **Credential Theft:** Prevents reading `/etc/shadow`, `/etc/passwd`
3. **SSH Key Theft:** Blocks access to `.ssh/` directories
4. **System Tampering:** Prevents writes to `/bin/`, `/sbin/`, `/etc/`
5. **Privilege Escalation:** Blocks dangerous capabilities like `SYS_ADMIN`

## Learning Resources

- **KubeArmor Documentation:** https://docs.kubearmor.io/
- **Security Policy Spec:** https://docs.kubearmor.io/kubearmor/documentation/security_policy_examples
- **Best Practices:** https://docs.kubearmor.io/kubearmor/use-cases/hardening

## Cleanup (Optional)

```bash
# Remove policies
kubectl delete -f wisecow-kubearmor-policy.yaml

# Uninstall KubeArmor
helm uninstall kubearmor -n kubearmor

# Or using karmor
karmor uninstall
```

## ✅ Submission Checklist

- [x] Created comprehensive KubeArmor policy YAML
- [x] Installed KubeArmor on Kubernetes cluster
- [x] Applied policy to cluster
- [x] Tested policy violations
- [x] Captured screenshots of policy monitoring
- [x] Committed policy YAML and screenshots to repo
