#!/bin/bash
# Script to configure the Heroku environment
echo "Setting up Flask app on Heroku..."
echo "Using Python $(python --version)"

# Use the simplified requirements file for Heroku
cp requirements_heroku.txt requirements.txt
