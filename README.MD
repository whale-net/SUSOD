# SUSOD
Super Ultra Server Of Doom

Web Service for running a local jukebox.


# Setup
**Requirements:**
- python3
- mysql-server
- ability to fill in the holes of this setup guide with your immense knowledge

## Setting up the environment
1. clone repository and cd into it `git clone https://github.com/whale-net/SUSOD.git && cd SUSOD`
2. Create python virtual environment `python3 -m venv env`
3. Actiavte virtual environment `source env/bin/activate`
4. Install requirements `python3 -m pip install -e .`
5. Give start script permissions `chmod +x ./bin/run`
6. Modify ./SUSOD/config.py 
7. follow guide to setup MySQL server and user account matching your config
8. `mysql -u DB_USERNAME -p DB_NAME < test_schema.sql`
9. `nodeenv --python-virtualenv`
10. `deactivate` to exist venv
11. `source env/bin/activate` to re-activate the venv
12. `npm install .` to install node modules

## Run the server from one window
* less screen clutter
* `npm run dev & ./bin/run` 

## OR Run the server from multiple windows
* easier error debugging
* `npm run dev` 
* `./bin/run`

### Finally
* Execute `./bin/run` and visit `http://localhost:8000/example`


# LICENSE
It's MIT. If somehow there is something you want to use in this repository, go ahead and use it, but let me know. I would just like to know how and where you use it.