# ============================================================================
# Dockerfile for Wisecow Application
# ============================================================================
# Author: Arpit Singh
# GitHub: @TSM-ArpitSG
# Purpose: Containerize the Wisecow bash application that serves random 
#          wisdom quotes with ASCII cow art via HTTP
# Base Image: Debian Bullseye Slim (lightweight)
# ============================================================================

# Use Debian slim as the base image (lightweight but has all the packages we need)
FROM debian:bullseye-slim

# Install required packages:
# - fortune-mod: generates random quotes
# - cowsay: displays quotes with ASCII cow art
# - netcat-openbsd: acts as the web server
# All these are available in Debian's default repositories
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fortune-mod \
    fortunes \
    cowsay \
    netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Add /usr/games to PATH so cowsay and fortune can be found
# (In Debian, these are installed in /usr/games by default)
ENV PATH="/usr/games:${PATH}"

# Create a directory for our application
WORKDIR /app

# Copy the wisecow.sh script from wisecow-app directory to the container
COPY wisecow-app/wisecow.sh /app/

# Make the script executable
RUN chmod +x /app/wisecow.sh

# Expose port 4499 (the port wisecow runs on)
EXPOSE 4499

# Run the wisecow script when container starts
CMD ["/app/wisecow.sh"]
