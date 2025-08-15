#!/bin/bash

# Wait for 30 seconds
sleep 5

# Navigate to your project directory
cd QPGen/ || exit 1

# Exit on error
set -e

echo "Starting the application..."
docker-compose start
