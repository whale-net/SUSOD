git clone https://github.com/whale-net/SUSOD.git && cd SUSOD
sudo apt-get update
sudo apt-get -y install python3-venv
python3 -m venv env
. env/bin/activate
python3 -m pip install -e .
chmod +x ./bin/run

nodeenv --python-virtualenv
deactivate
. env/bin/activate
npm install .

echo '\n\nPlease modify config.py to match your configuration.'