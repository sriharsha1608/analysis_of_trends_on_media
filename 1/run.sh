#!/bin/bash
set -a
source config.env
set +a
export PYTHONUNBUFFERED=yes
python3 twitter.py > twitter.log &
python3 reddit.py > reddit.output &
python3 hn.py > hn.output &
