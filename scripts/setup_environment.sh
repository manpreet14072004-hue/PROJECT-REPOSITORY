#!/bin/bash
# Setup environment script

echo "Setting up project environment..."

# Install conda environment
echo "Creating conda environment..."
conda env create -f environment.yml

# Activate environment
echo "Activating environment..."
source activate project-env

# Install pip dependencies
echo "Installing pip dependencies..."
pip install -r requirements.txt

echo "Environment setup complete!"
