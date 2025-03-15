#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt

# Initialize the database
python3 init_db.py

# Generate sample data
python3 generate_sample_data.py

echo "Setup complete! You can now run the application with ./run.sh" 