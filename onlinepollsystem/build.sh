#!/usr/bin/env bash
# build.sh - Render Build Script for Django Online Poll System

set -o errexit  # Exit on any error

echo "Starting build process for Django Online Poll System..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

echo "Build process completed successfully!"