#!/usr/bin/env bash

CURRENT_DIR=$(pwd)
SH_DIR=$(dirname "$0")
VENV_DIR=".pyenv"

# Go to server folder
cd $SH_DIR

# Create Python3 environment and activate it
virtualenv -p python3 $VENV_DIR
source $VENV_DIR/bin/activate

# Install requirements
pip install --no-cache -r requirements.txt

# Start CTT Server
python ctt-agent.py

deactivate

# Return to original folder
cd $CURRENT_DIR
