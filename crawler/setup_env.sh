#!/bin/bash
'''
# Ensure you have Python 3 and pip installed before running this script.
# Make this script executable with: chmod +x setup_env.sh
# This script sets up a virtual environment and installs the required packages.


'''

# Create a virtual environment named 'venv'
python3 -m venv venv


# Install requirements
pip install --upgrade pip
pip install -r requirements.txt

echo "Environment setup complete. To activate later, run: source venv/bin/activate"