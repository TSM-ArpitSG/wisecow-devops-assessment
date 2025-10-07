# Problem Statement 2: System Health Monitoring Scripts

**Status:** COMPLETE

**Author:** Arpit Singh  
**GitHub:** @TSM-ArpitSG

## Overview

This section contains 2 scripts implementing different monitoring and health check functionalities:

1. **System Health Monitoring Script** (Python) - Monitors CPU, memory, disk, and processes
2. **Application Health Checker** (Bash) - Checks application uptime via HTTP status codes

## Structure
problem-2/
├── README.md
├── script1.py (or .sh)
└── script2.py (or .sh)

---

## Script 1: System Health Monitor (Python)

### Purpose
Monitor Linux system health metrics and send alerts when predefined thresholds are exceeded.

### Features
- **CPU Usage Monitoring** - Alerts when CPU usage > 80%
- **Memory Usage Monitoring** - Alerts when memory usage > 80%
- **Disk Space Monitoring** - Alerts when disk usage > 80%
- **Process Monitoring** - Lists top 5 CPU-consuming processes
- **Colored Console Output** - Easy-to-read status indicators
- **Log File Generation** - All events logged to `system_health.log`

### Prerequisites
```bash
# Install required Python package
pip3 install psutil
```

### Usage
```bash
# Make executable
chmod +x system_health_monitor.py

# Run the monitor
python3 system_health_monitor.py

# Or directly execute
./system_health_monitor.py
```

### Configuration
Edit thresholds in the script:
```python
CPU_THRESHOLD = 80          # CPU usage percentage
MEMORY_THRESHOLD = 80       # Memory usage percentage
DISK_THRESHOLD = 80         # Disk usage percentage
```

### Example Output
```
======================================================================
System Health Monitoring Report
Generated at: 2025-10-07 11:30:45
======================================================================

[2025-10-07 11:30:45] [INFO] Starting system health monitoring...
[2025-10-07 11:30:46] [INFO] CPU Usage: 45.2%
[2025-10-07 11:30:46] [INFO] Memory Usage: 62.3% (Used: 10.5GB / Total: 16.0GB)
[2025-10-07 11:30:46] [INFO] Disk Usage: 55.8% (Used: 250.2GB / Total: 500.0GB)
[2025-10-07 11:30:46] [INFO] Total Running Processes: 342
[2025-10-07 11:30:46] [INFO] Top 5 CPU-consuming processes:

======================================================================
System Health: ALL CHECKS PASSED
======================================================================
```

### Exit Codes
- `0` - All checks passed
- `1` - One or more alerts triggered

---

## Script 2: Application Health Checker (Bash)

### Purpose
Check application uptime and health by monitoring HTTP status codes to determine if an application is 'up' or 'down'.

### Features
- **HTTP Status Code Analysis** - Comprehensive HTTP code handling
- **Connection Timeout** - 10-second timeout for responsiveness
- **Redirect Following** - Automatically follows HTTP redirects
- **Colored Output** - Visual status indicators (Green=UP, Red=DOWN, Yellow=Warning)
- **Log File Generation** - All checks logged to `app_health.log`
- **Flexible Usage** - Works with any HTTP/HTTPS endpoint

### Prerequisites
```bash
# curl should be pre-installed on most systems
# If not, install it:
# Ubuntu/Debian:
sudo apt-get install curl

# macOS (usually pre-installed):
brew install curl
```

### Usage
```bash
# Make executable
chmod +x app_health_checker.sh

# Check application health
./app_health_checker.sh <URL> [APPLICATION_NAME]

# Examples:
./app_health_checker.sh http://localhost:30080 Wisecow
./app_health_checker.sh https://wisecow.local Wisecow-TLS
./app_health_checker.sh https://google.com Google
```

### HTTP Status Code Handling
| Status Code Range | Status | Description |
|-------------------|--------|-------------|
| 200, 201, 202, 204 | UP | Application functioning correctly |
| 301, 302, 307, 308 | UP | Redirect (application accessible) |
| 400, 401, 403, 404 | DOWN | Client errors |
| 500, 502, 503, 504 | DOWN | Server errors |
| 000 | DOWN | Connection failed/timeout |
| Other | UNKNOWN | Unexpected status code |

### Example Output
```
======================================================================
Application Health Checker
Started at: 2025-10-07 11:35:22
======================================================================

[2025-10-07 11:35:22] [INFO] Checking application: Wisecow
[2025-10-07 11:35:22] [INFO] URL: http://localhost:30080
[2025-10-07 11:35:23] [SUCCESS] HTTP Status Code: 200 (OK)
[2025-10-07 11:35:23] [SUCCESS] Status: UP
[2025-10-07 11:35:23] [SUCCESS] Application 'Wisecow' is functioning correctly

======================================================================
Health Check: PASSED
======================================================================
```

### Exit Codes
- `0` - Application is UP and functioning
- `1` - Application is DOWN or error occurred
- `2` - Unknown status (unexpected HTTP code)

---

## Files in This Directory

```
problem-2/
├── README.md                    # This documentation
├── system_health_monitor.py     # Python system health monitoring script
├── app_health_checker.sh        # Bash application health checker script
├── system_health.log           # Log file (generated on first run)
└── app_health.log              # Log file (generated on first run)
```

---

## Testing Examples

### Test System Health Monitor
```bash
# Run system health check
python3 system_health_monitor.py

# Check the log file
cat system_health.log
```

### Test Application Health Checker
```bash
# Test with Wisecow application (if running)
./app_health_checker.sh http://localhost:30080 Wisecow

# Test with public website
./app_health_checker.sh https://google.com Google

# Test with non-existent endpoint (should show DOWN)
./app_health_checker.sh http://localhost:9999 NonExistent

# Check the log file
cat app_health.log
```

---

## Use Cases

### System Health Monitor
- **Server Monitoring**: Regular health checks on production servers
- **CI/CD Integration**: Pre-deployment health validation
- **Alerting**: Integration with monitoring systems (Prometheus, Grafana)
- **Capacity Planning**: Track resource usage trends over time

### Application Health Checker
- **Load Balancer Health Checks**: Verify backend application availability
- **Kubernetes Liveness Probes**: Integration with K8s health checks
- **Uptime Monitoring**: Regular application availability checks
- **Wisecow Integration**: Monitor the PS1 Wisecow application!

---

## Integration with Problem Statement 1

You can use the **Application Health Checker** to monitor the Wisecow application from PS1:

```bash
# Check if Wisecow is running (NodePort)
./app_health_checker.sh http://localhost:30080 Wisecow

# Check if Wisecow TLS is working
./app_health_checker.sh https://wisecow.local Wisecow-TLS
```

---

## Future Enhancements

- [ ] Add email/Slack notifications for alerts
- [ ] Implement continuous monitoring mode (loop with intervals)
- [ ] Add Prometheus metrics export
- [ ] Create Docker containers for both scripts
- [ ] Add Kubernetes CronJob manifests for scheduled execution
- [ ] Implement database storage for historical metrics

---

**Built with ❤️ for DevOps monitoring and observability**
