#!/bin/sh

[ ! $(which gem) ] && echo "gem not found in this system. Exiting." && exit 1
$(which gem) install wpscan
wpscan --update

[ ! $(which python3) ] && echo "python3 not found in this system. Exiting." && exit 1
python3 -m pip install virtualenv
virtualenv venv -p python3
. venv/bin/activate
pip install --no-cache-dir -r requirements.txt

[ ! $(which git) ] && echo "git not found in this system. Exiting." && exit 1
git submodule update --init --recursive
cd plugins/vbscan/ && git pull origin master
cd ../joomscan/ && git pull origin master
