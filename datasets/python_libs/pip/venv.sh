#!/bin/bash

# Create a mininal python virtual environment with updated
# pip-compile.

mkdir -p venv 
rm -rf venv 

echo 'creating new python3 virtual environment in the venv directory ...'
python3 -m venv venv

echo 'activating new venv ...'
source venv/bin/activate

echo 'upgrading pip ...'
python -m pip install --upgrade pip 

echo 'install pip-tools ...'
pip install --upgrade pip-tools

echo 'displaying python location and version'
which python
python --version

source venv/bin/activate
