#!/usr/bin/env python3

# ============================================================================
# System Health Monitoring Script
# ============================================================================
# Author: Arpit Singh
# GitHub: @TSM-ArpitSG
# Purpose: Monitor Linux system health metrics (CPU, Memory, Disk, Processes)
#          and send alerts when thresholds are exceeded
# ============================================================================

import psutil
import datetime
import sys
import os

# Configuration - Threshold values
CPU_THRESHOLD = 80          # CPU usage percentage
MEMORY_THRESHOLD = 80       # Memory usage percentage
DISK_THRESHOLD = 80         # Disk usage percentage
LOG_FILE = "system_health.log"

# ANSI color codes for console output
RED = '\033[91m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'


def log_message(message, level="INFO"):
    """Log message to both console and log file"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    
    # Console output with colors
    if level == "ALERT":
        print(f"{RED}{log_entry}{RESET}")
    elif level == "WARNING":
        print(f"{YELLOW}{log_entry}{RESET}")
    elif level == "SUCCESS":
        print(f"{GREEN}{log_entry}{RESET}")
    else:
        print(f"{BLUE}{log_entry}{RESET}")
    
    # Write to log file
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry + '\n')


def check_cpu_usage():
    """Monitor CPU usage"""
    cpu_percent = psutil.cpu_percent(interval=1)
    log_message(f"CPU Usage: {cpu_percent}%", "INFO")
    
    if cpu_percent > CPU_THRESHOLD:
        log_message(
            f"ALERT: CPU usage is {cpu_percent}% (Threshold: {CPU_THRESHOLD}%)",
            "ALERT"
        )
        return False
    return True


def check_memory_usage():
    """Monitor memory usage"""
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    log_message(
        f"Memory Usage: {memory_percent}% "
        f"(Used: {memory.used / (1024**3):.2f}GB / Total: {memory.total / (1024**3):.2f}GB)",
        "INFO"
    )
    
    if memory_percent > MEMORY_THRESHOLD:
        log_message(
            f"ALERT: Memory usage is {memory_percent}% (Threshold: {MEMORY_THRESHOLD}%)",
            "ALERT"
        )
        return False
    return True


def check_disk_usage():
    """Monitor disk space"""
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    log_message(
        f"Disk Usage: {disk_percent}% "
        f"(Used: {disk.used / (1024**3):.2f}GB / Total: {disk.total / (1024**3):.2f}GB)",
        "INFO"
    )
    
    if disk_percent > DISK_THRESHOLD:
        log_message(
            f"ALERT: Disk usage is {disk_percent}% (Threshold: {DISK_THRESHOLD}%)",
            "ALERT"
        )
        return False
    return True


def check_running_processes():
    """Monitor running processes"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Sort by CPU usage
    processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
    
    log_message(f"Total Running Processes: {len(processes)}", "INFO")
    log_message("Top 5 CPU-consuming processes:", "INFO")
    
    for i, proc in enumerate(processes[:5], 1):
        cpu = proc['cpu_percent'] if proc['cpu_percent'] is not None else 0.0
        mem = proc['memory_percent'] if proc['memory_percent'] is not None else 0.0
        log_message(
            f"  {i}. PID: {proc['pid']}, Name: {proc['name']}, "
            f"CPU: {cpu:.1f}%, Memory: {mem:.1f}%",
            "INFO"
        )
    
    return True


def print_header():
    """Print monitoring header"""
    print("\n" + "=" * 70)
    print(f"{BLUE}System Health Monitoring Report{RESET}")
    print(f"{BLUE}Generated at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print("=" * 70 + "\n")


def print_summary(all_healthy):
    """Print summary"""
    print("\n" + "=" * 70)
    if all_healthy:
        print(f"{GREEN}✓ System Health: ALL CHECKS PASSED{RESET}")
    else:
        print(f"{RED}✗ System Health: ALERTS DETECTED - Check logs for details{RESET}")
    print("=" * 70 + "\n")


def main():
    """Main monitoring function"""
    print_header()
    
    log_message("Starting system health monitoring...", "INFO")
    
    # Run all checks
    cpu_ok = check_cpu_usage()
    memory_ok = check_memory_usage()
    disk_ok = check_disk_usage()
    processes_ok = check_running_processes()
    
    all_healthy = cpu_ok and memory_ok and disk_ok and processes_ok
    
    print_summary(all_healthy)
    log_message("System health monitoring completed.", "SUCCESS")
    
    # Exit with appropriate code
    sys.exit(0 if all_healthy else 1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nMonitoring interrupted by user.")
        sys.exit(0)
    except Exception as e:
        log_message(f"ERROR: {str(e)}", "ALERT")
        sys.exit(1)
