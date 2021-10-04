# python-misc
Misc Python scripts that I've written.

### GDQScrape.py

This file is used for scraping donations on the Games Done Quick (GDQ) site for an inputted year and inputted event (Awesome Games Done Quick or Summer Games Done Quick (AGDQ/SGDQ)).  This data is exported as CSV for later use with Pandas or Microsoft Power BI.

### GetGPSCords.py

This file works with my .shp file (you can point it to your own file) which is a file that contains geographic points that make up polygons.  The script will run through the entire .shp file and get the center lat/long of the bounding box (this is a box that could fit the entire polygon within it) and prints that to a series of CSV files.  These CSV files are limited to 2000 rows per file so they can be uploaded to Google maps for adding pins to a map.  I currently use this to point out all locations that I have updated in Indiana in Microsoft Flight Simulator.  Link here to see how that looks: https://www.google.com/maps/d/u/0/edit?mid=17pRdp7RXoddxQ43SRUQCeIvOmlx8DDMR&usp=sharing

### IndeedScraper.py

Scrapes jobs on Indeed based on an entered serach term and location.  Prints the Job Name, Job Company, Job Location, and link to the Indeed site in a CSV file for easier parsing.

### espnscrape.py

Scraper for college football standings and stats for a given season.  Works for all 4 divisions at https://www.espn.com/college-football/standings/_/ . Outputs in a CSV for later data analysis for for importing into Pandas in a different script.

### helpful

Some helpful stuff I found on Reddit that I have to reach through.

### sportsReferenceScrape.py

Similar to the ESPN scraper, scrapes Sports Reference for stats over time and outputs to a CSV file.

## RS Wiki Prices

### rs-profitableAlchs

Using the latest prices, display a table of items that are profitable to buy from the G.E. and high alch.  Gives the limit of the item as well as profit per item.

## Regression Analysis

### KNearestCarData

Using the K Nearest Neighbors algorithim, predict the class of a car in the car.data dataset given a handful of different variables.

### StudentDataRegression

Using linear regression and the student data set, find the coefficients for different variables to find their overall effect on the prediction of the final class grade. 
