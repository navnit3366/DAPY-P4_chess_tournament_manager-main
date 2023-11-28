# tournament_manager tournaments manager

Marie Jeammet - v1.0 - 2021/08.

Contact : marie.jeammet@protonmail.com

## Context

Offline tool for tournaments management. Answers to commandline input. 

This project using Python 3.6.9 and tinydb version 4.5.1

## Installation
### Cloning the project

Clone project the project to desired location:

`$ git clone https://github.com/mjeammet/OC_P4.git`

### Setting the environment

In the project's directory, create and activate the environment:

`$ python3 -m venv env`

`$ source env/bin/activate`

and install required packages with:

`$ pip install -r requirements.txt`

##  Usage

Once you've activated your environment and made sure all required packages are correctly set up, go and run:

`$ python main.py`

Follow textual instructions on the screen to 
- Add players and tournaments to database
- Add players to tournament
- Starts a new round and add round results
- Prints reports on players, tournaments, rounds and matches 

To navigate, simply enter the number corresponding to your next desired action. 

## Flake8

flake8 was used in this projet to make sure PEP 8 recommandations where followed. 

To generate a new report : 

`$ flake8 --format=html --htmldir=flake8_rapport --max-line-length 119 --exclude env,__pycache__,__init__.py`
