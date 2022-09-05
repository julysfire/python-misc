# Brief File Explanations
Misc Python scripts that I've written.

### letterQuestHelper.py

This script is for use with the game: Letter Quest: Grimm's Journey (and the Remastered Edition).  The game is a scrabble-like game and this script will help find word combinations and their scores.  The script listens for the key "F2" to be pressed in order to activate.  First, the script will check if the game is running and if so, grab a screenshot of the location where the letters are stored during play.  It will then crop the image to get each of the individual letters and then run them through Tesseract OCR to determine which letter is in each image.  Once it determines the set of letters that you have, it will search a dictionary file (Scrabble.txt) that contains a list of words that are acceptable for Scrabble and determine what words can be created.  It will score each word and then output each of the possible words and their scores in the console, divided into sections based on the length of the word.  

### sponsorBlockStats.py

This script is for getting your stats for SponsorBlock (https://chrome.google.com/webstore/detail/sponsorblock-for-youtube/mnjggcdmjocbbbhaepdhchncahnbgone?hl=en) using the built in API endpoints.  The script will get information such as the segments you have submitted, the categories those segments belong to, the total amount of time you have saved people and the total amount of views your segments have.  The dat awill be saved to a .csv file in your desired location.  This makes it wasy to create a .bat file and schedule it to run so that you can see your stats over time.

Required arguments:
- publicUserID: Your SponsorBlock public ID (You can copy yours from the SponorBlock icon under "Your Work", 3rd icon.  It should be a 64 character long string.
- fileSaveLocation: Where you want to save your file.  For Example: "C:\Users\JoeSmo\Desktop\"

Example running the file: `python "D:\pathToFile\sponsorBlockStats.py" "1234567890abcdefgh" "C:\Users\JoeSmo\Desktop\"`

### GDQScrape.py

This file is used for scraping donations on the Games Done Quick (GDQ) site for an inputted year and inputted event (Awesome Games Done Quick or Summer Games Done Quick (AGDQ/SGDQ)).  This data is exported as CSV for later use with Pandas or Microsoft Power BI.

### GetGPSCords.py

This file works with my .shp file (you can point it to your own file) which is a file that contains geographic points that make up polygons.  The script will run through the entire .shp file and get the center lat/long of the bounding box (this is a box that could fit the entire polygon within it) and prints that to a series of CSV files.  These CSV files are limited to 2000 rows per file so they can be uploaded to Google maps for adding pins to a map.  I currently use this to point out all locations that I have updated in Indiana in Microsoft Flight Simulator.  Link here to see how that looks: https://www.google.com/maps/d/u/0/edit?mid=17pRdp7RXoddxQ43SRUQCeIvOmlx8DDMR&usp=sharing

### IndeedScraper.py

Scrapes jobs on Indeed based on an entered serach term and location.  Prints the Job Name, Job Company, Job Location, and link to the Indeed site in a CSV file for easier parsing.

### espnscrape.py

Scraper for college football standings and stats for a given season.  Works for all 4 divisions at https://www.espn.com/college-football/standings/_/ . Outputs in a CSV for later data analysis for for importing into Pandas in a different script.

### sportsReferenceScrape.py

Similar to the ESPN scraper, scrapes Sports Reference for stats over time and outputs to a CSV file.

### helpful

Some helpful stuff I found on Reddit that I have to reach through.

### EmptyFolderRemove.py

Takes a single input of a directory.  The directory will be looped through and any folders that do not have files in them will be deleted.

### dupefinder.py

Takes a single input of the directory to be searched for duplicate files.  The files will be hashed and then checked for uniqueness.  Any duplicate files will be deleted.  Works for all sub folders within the directory given.  Great when paired with EmptyFolderRemove to delete sub directories that are empty.

### steamAchievementStats

This script reaches out to the Steam API to get all achievements for all owned games on your Steam account and inserts the data into a MySQL table to allow easy data analysis.  A lot of this fiile uses personal data such as MySQL server connection/logins and private Steam profile ids and API keys so this is more of a cut back version so you can get an idea on how to perform an operation like this.

###CryptoPriceNotify.py

This script reaches out to the coinbase API to get the exchange rates for BTC, BAT and DOGE in USD and then displays a toast for the percent change over time from when the script started.  This will run ever hour on the hour and give at toast then with a percent change from the previous hour.

## RS Wiki

### rs-profitableAlchs

Using the latest prices, display a table of items that are profitable to buy from the G.E. and high alch.  Gives the limit of the item as well as profit per item.

### OSRSMusicTrackScrape

Scrapes the OSRS wiki for the full list of music tracks in OSRS and the instructions for unlocking said track.

## Regression Analysis

### KNearestCarData

Using the K Nearest Neighbors algorithim, predict the class of a car in the car.data dataset given a handful of different variables.

### StudentDataRegression

Using linear regression and the student data set, find the coefficients for different variables to find their overall effect on the prediction of the final class grade. 
