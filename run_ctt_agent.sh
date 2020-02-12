#!/usr/bin/env bash

CURRENT_DIR=$(pwd)
SH_DIR=$(dirname "$0")

cd $SH_DIR
virtualenv .
source bin/activate
pip install --no-cache -r requirements.txt
python ctt-agent.py
