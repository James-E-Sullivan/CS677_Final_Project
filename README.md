Destiny 2 Data Analysis
-

Created by James E. Sullivan
 - email: jesull2@bu.edu
 - CS 677, Summer O2

The purpose of this program is the following:
1. Connect to the Bungie API for Destiny 2
2. Obtain historical data from competitive crucible (aka PvP (player vs player))
matches for specified Destiny 2 accounts
3. Compile historical match data into a format that can be analyzed (pandas 
DataFrame)
4. Analyze data and output results 

Connecting to the Bungie API
* Code related to the Bungie API is stored in data_collection.bungie_api.py.
* The API Key stored in HEADERS is an API key for only this project. 
* bungie_api.py contains functions used for calls to the bungie API
    * bungie.net returns json strings that need to be parsed 
    
Obtaining Historical Match Data
* Historical match id values need to be obtained first (on a per character, per
account basis)
* Match id values can then be used to obtain PostGameCarnageReport (PGCR) data, 
which includes game-specific statistics for all players in the game
* Weapon id's and use statistics can be found in the PGCR extended data
    * Weapon descriptions can only be found in Destiny2 manifest
    * For this program, I have downloaded a portion of the English manifest
    and added it to the directory
    * For ease of use, the DestinyInventoryItemDescription table has been
    converted into a dictionary
    
Compilation of Match Data into Useful Format
* Game data obtained from each PGCR is added to a DataFrame for each Account
* Account specific DataFrames are then saved as CSV files in
 data_collection/match_datasets
* Data-sets can be generated or updated by running dataio.py

Analysis of Match Data
* Running project_main.py will open match data csv files as Pandas DataFrames
* Each df is split into 2 approximately equal halves (training/prediction sets)
* These sets are fed into functions that predict values for the prediction sets
using logistic regression or linear SVM classifiers
* The accuracy of predicted values is analyzed, and findings are output to 
the console
* Each user's top weapons (per-game) are analyzed by average win-rate. Highest
win-rate weapons for each user is also output to console
