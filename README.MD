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

## Windows Setup
1. clone repository from git
2. Install python3 for windows https://www.python.org/downloads/windows/ 
3. Add python to Path. Add the following to the Path with changed values for X, replaced with version, and Your Username. This can be accessed by  `Start Menu -> "View Advanced System Settings" -> EnvironmentVariables -> Path -> Edit`
	a. `C:\Users\YOUR_USERNAME\AppData\Local\Programs\Python\Python3X`
	b. `C:\Users\YOUR_USERNAME\AppData\Local\Programs\Python\Python3X\Scripts`
4. From a PowerShell window, create python virtual environment `python -m venv env`
5. Activate environment ` .\env\Scripts\activate`
6. Install requirements `python -m pip install -e .`
7. `deactivate` to exist venv
8. Install npm and add to path, recommended to use chocolatey https://chocolatey.org/, run `choco install nodejs`
9. From a separate PowerShell window activate environment ` SUSOD_DIRECTORY\env\Scripts\activate.ps1`
10. `nodeenv --python-virtualenv`
11. `npm run dev` 

## Windows PyCharm
1. In PyCharm File -> Settings-> Tools -> Terminal -> change Shell path to `c:\Windows\system32\WindowsPowerShell\v1.0\powershell.exe`
2. Set up a run config from `Run -> Edit Configurations...`
	a. Add new "Shell Script", set the "Script path" to `C:\...\SUSOD\winRun.ps1`
	b. You may need to change your ExecutionPolicy to be allowed to execute scipts. From a powershell window, with admin permissions, run `Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser`
		i. Always read scripts before running them!
3. Run with Green play button at top right, with new configuration set
4. The debugger can be attached after from `Run->Attach To Process...`



## Run the server from one window
* less screen clutter
* `npm run dev & ./bin/run` 

## OR Run the server from multiple windows
* easier error debugging
* `npm run dev` 
* `./bin/run`

### Finally
* Execute `./bin/run` and visit `http://localhost:8000/example`

at some point update this to include
https://stackoverflow.com/questions/1884859/lost-connection-to-mysql-server-during-query
The mysql docs have a whole page dedicated to this error:
http://dev.mysql.com/doc/refman/5.0/en/gone-away.html

of note are

 - You can also get these errors if you send a query to the server that is incorrect or too large. If mysqld receives a packet that is too large or out of order, it assumes that something has gone wrong with the client and closes the connection. If you need big queries (for example, if you are working with big BLOB columns), you can increase the query limit by setting the server's max_allowed_packet variable, which has a default value of 1MB. You may also need to increase the maximum packet size on the client end. More information on setting the packet size is given in Section B.5.2.10, “Packet too large”.
 

 - You can get more information about the lost connections by starting mysqld with the --log-warnings=2 option. This logs some of the disconnected errors in the hostname.err file




# LICENSE
It's MIT. If somehow there is something you want to use in this repository, go ahead and use it, but let me know. I would just like to know how and where you use it.