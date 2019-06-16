# SUSOD
Super Ultra Server Of Doom

Web Service for running a local jukebox.


# Setup
**Requirements:**
- python3
- mysql-server
- ability to fill in the holes of this setup guide with your immense knowledge

1. clone repository and cd into it `git clone https://github.com/whale-net/SUSOD.git && cd SUSOD`
2. Create python virtual environment `python3 -m venv env`
3. Actiavte virtual environment `source env/bin/activate`
4. Install requirements `python3 -m pip install -e .`
5. Give start script permissions `chmod +x ./bin/run`
6. Modify ./SUSOD/config.py 
7. follow guide to setup MySQL server and user account matching your config
8. Execute `./bin/run` and visit `http://localhost:8000`
