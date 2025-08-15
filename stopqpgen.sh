#!/bin/bash

# Navigate to your project directory
cd QPGen/ || exit 1

# Exit on error
set -e

echo "Stopping the application..."
docker-compose stop

echo "Application stopped."