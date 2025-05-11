#!/bin/bash

# Navigate to the project directory
cd /Users/cynthiamatutelopez/NovaBotLocal/nova-proxy

# Activate virtual environment
source venv/bin/activate

# Run the verification monitor
python monitor_verifications.py

# Deactivate virtual environment
deactivate 