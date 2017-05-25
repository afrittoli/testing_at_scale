#!/bin/bash

BASE_DIR=$(cd $(dirname $0); pwd)
VENV=${BASE_DIR}/.jpc

if [ ! -d $VENV ]; then
    python3 -mvenv $VENV
fi

source $VENV/bin/activate
pip install -r $BASE_DIR/requirements.txt

python $BASE_DIR/jobs_per_change.py --config-file $BASE_DIR/subunit2sql.conf