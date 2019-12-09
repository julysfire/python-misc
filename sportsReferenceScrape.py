import os
from datetime import date

#Get packages
try:
    import requests
    import pandas as pd
except ImportError:
    os.system('pip install pandas')
    os.system('pip install requests')
    import requests
    import pandas as pd

def scrapeSchedule(year):
    print("Year: " + str(year))
    #Variables
    fullTble = [[]]
    looper = True
    tempX = counter = 0

    #Get HTML
    y = requests.get("https://www.sports-reference.com/cfb/years/"+str(year)+"-schedule.html").text

    while looper:
        x = y.find('<th scope="row" class="right " data-stat="ranker"',0,len(y))
        z = y[x:y.find('<th scope="row" class="right " data-stat="ranker"',x+45,len(y))]
        tempArray = []

        #TODO: For winner team and loser team, get around href check
        if x > 0:
            #Rk
            counter = counter + 1
            tempArray.append(counter)

            #Wk
            tempX = z.find("week_number",0,len(z))
            tempArray.append(z[z.find(">",tempX,len(z))+1:z.find("<",tempX,len(z))])
            tempX = z.find("href=",z.find("date_game",tempX+6,len(z)),len(z))

            #Date
            tempArray.append(z[z.find(">",tempX,len(z))+1:z.find("<",tempX,len(z))])
            tempX = z.find("time_game",tempX+6,len(z))

            #Older dates don't have timestamps
            if tempX == -1:
                tempX = 0

            #Time
            tempArray.append(z[z.find(">",tempX,len(z))+1:z.find("<",tempX,len(z))])
            tempX = z.find("day_name",tempX,len(z))

            #Day
            tempArray.append(z[z.find(">",tempX,len(z))+1:z.find("<",tempX,len(z))])
            tempX = z.find("href=",z.find("winner_school_name",tempX+6,len(z)),len(z))
            checkX = z.find("winner_points",0,len(z))

            #Winner
            #Check if no href link
            if checkX < tempX:
                tempX = z.find("winner_school_name",0,len(z))
            tempArray.append(z[z.find(">",tempX,len(z))+1:z.find("<",tempX,len(z))])
            tempX = z.find("winner_points",tempX,len(z))

            #WinnerPts
            tempArray.append(z[z.find(">",tempX,len(z))+1:z.find("<",tempX,len(z))])
            tempX = z.find("game_location",tempX,len(z))

            #@
            tempArray.append(z[z.find(">",tempX,len(z))+1:z.find("<",tempX,len(z))])
            tempX = z.find("href=", z.find("loser_school_name", tempX + 6, len(z)), len(z))

            #Loser
            #Check if no href link
            if tempX < 0:
                tempX = z.find("loser_school_name",0,len(z))
            tempArray.append(z[z.find(">",tempX,len(z))+1:z.find("<",tempX,len(z))])
            tempX = z.find("loser_points",tempX,len(z))

            #Loser Pts
            tempArray.append(z[z.find(">",tempX,len(z))+1:z.find("<",tempX,len(z))])
            tempX = z.find("notes",tempX,len(z))

            #Notes
            tempArray.append(z[z.find(">",tempX,len(z))+1:z.find("<",tempX,len(z))])
            fullTble.append(tempArray)
        else:
            looper = False
        y = y[x+100:len(y)]

    fullTble.pop(0)
    counter = 0
    return fullTble


#Get current year
year = date.today().year
if 0 < date.today().month < 9:
    year = year - 1

#Location input
location = input("Enter a path to where you would like to save the CSV file: ")
if location[len(location)-1] != "\\":
    location = location + "\\"
if os.path.isdir(location) == False:
    print("Path entered does not exist.")
    exit()

toDate = input("Please enter the year of the date your wish to scrape to (2019- ): ")
toDate = int(toDate)
if toDate < 1870:
    print("Unable to go back further then that.")
    exit()

#Dataframe
df = pd.DataFrame(columns=["Rk","Week", "Date", "Time", "Day", "Winner", "Winner Pts", "@", "Loser", "Loser Pts", "Notes"])

#Main loop to call function
while year > toDate:
    x = scrapeSchedule(year)
    year = year - 1
    df2 = pd.DataFrame(data=x,columns=["Rk","Week", "Date", "Time", "Day", "Winner", "Winner Pts", "@", "Loser", "Loser Pts", "Notes"])
    df = df.append(df2,ignore_index=True)

#Save out
print(df.to_string)
export_csv = df.to_csv(location+"sportsReferenceScrape.csv",index=None,header=True)
