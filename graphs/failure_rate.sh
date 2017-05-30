#!/bin/bash

BASE_DIR=$(cd $(dirname $0); pwd)
VENV=${BASE_DIR}/.graphs

if [ ! -d $VENV ]; then
    python3 -mvenv $VENV
fi

# Get the zuul all_jobs graph
curl "http://graphite.openstack.org/render/?from=-150days&until=now&target=movingAverage(asPercent(transformNull(stats_counts.zuul.pipeline.gate.job.gate-tempest-dsvm-neutron-full-ubuntu-xenial.FAILURE),transformNull(sum(stats_counts.zuul.pipeline.gate.job.gate-tempest-dsvm-neutron-full-ubuntu-xenial.%7BSUCCESS,FAILURE%7D))),'1d')&format=csv" | awk -F',' '{ print $7","$8 }' > $BASE_DIR/failure_rate.csv

source $VENV/bin/activate
pip install -r $BASE_DIR/requirements.txt

python $BASE_DIR/failure_rate.py
