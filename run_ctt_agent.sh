#!/usr/bin/env sh

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

# Look for requirements.txt files in the 'plugins' folder and install them
PLUGIN_REQ_FILES=$(find plugins -iname "requirements.txt" -type f)
for req_file in $PLUGIN_REQ_FILES
do
   pip install --no-cache -r $req_file
done

# Start CTT Server
python3 ctt-agent.py

deactivate

# Return to original folder
cd $CURRENT_DIR

