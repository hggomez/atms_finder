All of this is meant to be run using bash.  
You need to setup two environment variables:
* `ATM_BOT_TOKEN`: your bot's token.
* `ATM_GOOGLE_MAPS_TOKEN`: your google map's token.  
Run `setup.sh` in order to generate a python virtualenv and setup the database.  
Run `source atms_env/bin/activate` in order to load the enviroment variables.  
Run `python3 atm_bot.py` in order to run the bot.