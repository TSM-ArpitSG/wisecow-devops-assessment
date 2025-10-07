#!/usr/bin/env bash

# ============================================================================
# Application Health Checker Script
# ============================================================================
# Author: Arpit Singh
# GitHub: @TSM-ArpitSG
# Purpose: Check application uptime and health via HTTP status codes
#          Determine if application is 'up' (functioning) or 'down' (unavailable)
# ============================================================================

# Configuration
LOG_FILE="app_health.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to log messages
log_message() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local log_entry="[$timestamp] [$level] $message"
    
    echo "$log_entry" >> "$LOG_FILE"
    
    case $level in
        "SUCCESS")
            echo -e "${GREEN}${log_entry}${NC}"
            ;;
        "ERROR")
            echo -e "${RED}${log_entry}${NC}"
            ;;
        "WARNING")
            echo -e "${YELLOW}${log_entry}${NC}"
            ;;
        *)
            echo -e "${BLUE}${log_entry}${NC}"
            ;;
    esac
}

# Function to print header
print_header() {
    echo ""
    echo "======================================================================"
    echo "Application Health Checker"
    echo "Started at: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "======================================================================"
    echo ""
}

# Function to check application health
check_application() {
    local url=$1
    local app_name=$2
    
    log_message "INFO" "Checking application: $app_name"
    log_message "INFO" "URL: $url"
    
    # Use curl to check HTTP status code
    # -s: silent mode
    # -o /dev/null: discard output
    # -w "%{http_code}": write out HTTP status code
    # --connect-timeout: connection timeout in seconds
    # -L: follow redirects
    
    http_code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 10 -L "$url" 2>/dev/null)
    curl_exit_code=$?
    
    # Check if curl command succeeded
    if [ $curl_exit_code -ne 0 ]; then
        log_message "ERROR" "Failed to connect to $url (curl exit code: $curl_exit_code)"
        log_message "ERROR" "Status: DOWN ❌"
        return 1
    fi
    
    # Analyze HTTP status code
    case $http_code in
        200|201|202|204)
            log_message "SUCCESS" "HTTP Status Code: $http_code (OK)"
            log_message "SUCCESS" "Status: UP ✓"
            log_message "SUCCESS" "Application '$app_name' is functioning correctly"
            return 0
            ;;
        301|302|307|308)
            log_message "WARNING" "HTTP Status Code: $http_code (Redirect)"
            log_message "WARNING" "Status: UP (but redirecting) ⚠"
            return 0
            ;;
        400|401|403|404)
            log_message "ERROR" "HTTP Status Code: $http_code (Client Error)"
            log_message "ERROR" "Status: DOWN ❌"
            log_message "ERROR" "Application '$app_name' returned client error"
            return 1
            ;;
        500|502|503|504)
            log_message "ERROR" "HTTP Status Code: $http_code (Server Error)"
            log_message "ERROR" "Status: DOWN ❌"
            log_message "ERROR" "Application '$app_name' is experiencing server errors"
            return 1
            ;;
        000)
            log_message "ERROR" "HTTP Status Code: 000 (Connection Failed)"
            log_message "ERROR" "Status: DOWN ❌"
            log_message "ERROR" "Unable to reach '$app_name' - Connection refused or timeout"
            return 1
            ;;
        *)
            log_message "WARNING" "HTTP Status Code: $http_code (Unknown)"
            log_message "WARNING" "Status: UNKNOWN ⚠"
            log_message "WARNING" "Application '$app_name' returned unexpected status code"
            return 2
            ;;
    esac
}

# Function to print usage
print_usage() {
    echo "Usage: $0 <URL> [APPLICATION_NAME]"
    echo ""
    echo "Examples:"
    echo "  $0 http://localhost:30080 Wisecow"
    echo "  $0 https://wisecow.local Wisecow-TLS"
    echo "  $0 https://google.com Google"
    echo ""
    exit 1
}

# Function to print summary
print_summary() {
    local status=$1
    echo ""
    echo "======================================================================"
    if [ $status -eq 0 ]; then
        echo -e "${GREEN}✓ Health Check: PASSED${NC}"
    elif [ $status -eq 2 ]; then
        echo -e "${YELLOW}⚠ Health Check: UNKNOWN STATUS${NC}"
    else
        echo -e "${RED}✗ Health Check: FAILED${NC}"
    fi
    echo "======================================================================"
    echo ""
}

# Main function
main() {
    # Check if URL is provided
    if [ -z "$1" ]; then
        print_usage
    fi
    
    local url=$1
    local app_name=${2:-"Application"}
    
    print_header
    
    # Check application
    check_application "$url" "$app_name"
    local status=$?
    
    print_summary $status
    
    log_message "INFO" "Health check completed with exit code: $status"
    
    exit $status
}

# Run main function
main "$@"
