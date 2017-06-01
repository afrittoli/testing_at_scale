#!/bin/bash

BASE_DIR=$(cd $(dirname $0); pwd)
VENV=${BASE_DIR}/.graphs

if [ ! -d $VENV ]; then
    python3 -mvenv $VENV
fi

source $VENV/bin/activate
pip install -r $BASE_DIR/requirements.txt

subunit2sql-graph --start-date 2017-01-01 --title "Test Volume Patter run time" --output ${BASE_DIR}/../runtime_variance.png --config-file ${BASE_DIR}/subunit2sql.conf run_time tempest.scenario.test_volume_boot_pattern.TestVolumeBootPattern.test_volume_boot_pattern
