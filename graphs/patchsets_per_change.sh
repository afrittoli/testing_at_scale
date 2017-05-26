#!/bin/bash

BASE_DIR=$(cd $(dirname $0); pwd)
VENV=${BASE_DIR}/.graphs

if [ ! -d $VENV ]; then
    python3 -mvenv $VENV
fi

source $VENV/bin/activate
pip install -r $BASE_DIR/requirements.txt

python $BASE_DIR/patchsets_per_change.py
