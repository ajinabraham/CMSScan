gem install wpscan
wpscan --update
python3 -m pip install virtualenv
virtualenv venv -p python3
. venv/bin/activate
pip install --no-cache-dir -r requirements.txt
# git submodule add https://github.com/rezasp/vbscan.git plugins/vbscan
# git submodule update --init --recursive
