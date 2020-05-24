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

# Windows Setup

## Setting up the environment
0. Easier with use of chocolatey, though it is not necessary https://chocolatey.org/
0. Commands need to be ran using PowerShell, not Command Prompt
1. Install git, can be installed from chocolatey `choco install git`
2. clone repository and cd into it `git clone https://github.com/whale-net/SUSOD.git && cd SUSOD`
3. Install python3 for windows https://www.python.org/downloads/windows/ 
4. Add python to Path. Needs to be ran in PowerShell, replace the X with your version
 		`[Environment]::SetEnvironmentVariable("Path", "$env:Path;%USERPROFILE%\AppData\Local\Programs\Python\Python3X", "User")` and 
 		`[Environment]::SetEnvironmentVariable("Path", "$env:Path;%USERPROFILE%\AppData\Local\Programs\Python\Python3X\Scripts", "User")`
5. Create virtual environment in project root `python -m venv env`
6. Activate environment ` .\env\Scripts\activate`
7. Install requirements `python -m pip install -e .`
8. `deactivate` to exist venv
9. Install nodejs and add npm to path, recommended to use chocolatey, run `choco install nodejs`
10.	`[Environment]::SetEnvironmentVariable("Path", "$env:Path;%USERPROFILE%\AppData\Roaming\npm\", "User")`
11. From a separate PowerShell window activate environment of directory in project root `.\env\Scripts\activate.ps1`
12. `nodeenv --python-virtualenv`
13. `deactivate` to exist venv
14. `.\env\Scripts\activate.ps1` to re-activate the venv
15. `npm install .` to install node modules

## Running the server
* `winRun.ps1` to activate the venv, set environment variables, and start flask
* `winRun_npm.ps1` to activate venv and start npm


## Windows PyCharm
1. In PyCharm File -> Settings-> Tools -> Terminal -> change Shell path to `c:\Windows\system32\WindowsPowerShell\v1.0\powershell.exe`
2. Set up a run config from `Run -> Edit Configurations...`
3. Add new "Shell Script", set the "Script path" to `C:\...\SUSOD\winRun.ps1`
4. Add new "Shell Script", set the "Script path" to `C:\...\SUSOD\winRun_npm.ps1` 
5. You may need to change your ExecutionPolicy to be allowed to execute scipts. From a powershell window, with admin permissions, run `Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser`
		
3. Run with Green play button at top right, with new configuration set
4. The debugger can be attached after from `Run->Attach To Process...`

at some point update this to include
https://stackoverflow.com/questions/1884859/lost-connection-to-mysql-server-during-query
The mysql docs have a whole page dedicated to this error:
http://dev.mysql.com/doc/refman/5.0/en/gone-away.html

of note are

 - You can also get these errors if you send a query to the server that is incorrect or too large. If mysqld receives a packet that is too large or out of order, it assumes that something has gone wrong with the client and closes the connection. If you need big queries (for example, if you are working with big BLOB columns), you can increase the query limit by setting the server's max_allowed_packet variable, which has a default value of 1MB. You may also need to increase the maximum packet size on the client end. More information on setting the packet size is given in Section B.5.2.10, “Packet too large”.
 

 - You can get more information about the lost connections by starting mysqld with the --log-warnings=2 option. This logs some of the disconnected errors in the hostname.err file




# LICENSE
It's MIT. If somehow there is something you want to use in this repository, go ahead and use it, but let me know. I would just like to know how and where you use it.