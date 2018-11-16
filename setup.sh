#!/bin/sh
gem install wpscan
wpscan --update
python3 -m pip install virtualenv
virtualenv venv -p python3
. venv/bin/activate
pip install --no-cache-dir -r requirements.txt
git submodule update --init --recursive
cd plugins/vbscan/ && git pull origin master
cd ../joomscan/ && git pull origin master