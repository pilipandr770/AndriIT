#!/bin/bash

# Script to initialize heroku deployment 
echo "Setting up Flask Shop for Heroku deployment..."

# Copy Heroku-specific requirements to main requirements.txt
cp requirements_heroku.txt requirements.txt

echo "Heroku initialization complete!"
