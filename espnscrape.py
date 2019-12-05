#import pip._internal.main
from datetime import date
from sys import exit

#pip._internal.main(['install','requests'])
#pip._internal.main(['install','pandas'])

#try:
import requests
import pandas as pd
#except ImportError:
#    print("Failed to install requests and pandas")

def scrapeESPNYear(year):
    #Tables
    tbleTitles = []
    tble = []
    statTble = [[]]
    tempArray = ["","","","","","","","",""]

    #Extra variables for finding text
    looper = True
    x = statFind = altFind = 1
    addCounter = placeCounter = cHolder = divFinder = 0
    confHolder = 0

    print("Year: " + str(year))
    y = requests.get("https://www.espn.com/college-football/standings/_/season/"+str(year)+"/view/fcs").text

    #Main loop
    while looper:
        x = y.find("Table__Title",x+1,len(y))

        if x > 0:
            #Table titles
            tbleTitles.append(y[x+14:y.find("</div>",x+1,len(y))])
            x=x+20
            confHolder = len(statTble)

            #Stat-cell is for the stats, alt-find is for finding the team names
            #When altFind > statFind, end of the teams listed for the given table
            statFind = y.find("stat-cell",x,len(y))
            altFind = x

            while altFind < statFind:
                altFind = y.find("alt=",altFind,len(y))

                #Found team name
                if altFind < statFind:
                    tble.append(y[altFind+5:y.find(" title=",altFind,len(y))-1])

                    #&amp;
                    if(tble[len(tble)-1].find("amp;")) > 0:
                        tble[len(tble)-1] = tble[len(tble)-1].replace("&amp;","&")
                    #For later to allocate stats per team
                    addCounter = addCounter + 1
                    altFind = altFind + 5
                else:
                    #Loop through the stats
                    for i in range(addCounter*7):
                        #W/L needs to be split
                        if placeCounter == 0 or placeCounter == 4:
                            midFinder = y[statFind+11:y.find("<",statFind,len(y))]
                            if midFinder == "--":
                                tempArray[placeCounter] = "0"
                                tempArray[placeCounter+1] = "0"
                            else:
                                divFinder = midFinder.find("-",1,len(midFinder))
                                tempArray[placeCounter] = midFinder[0:divFinder]
                                tempArray[placeCounter+1] = midFinder[divFinder:len(midFinder)]
                            placeCounter = placeCounter + 2
                        #Otherwise throw it into the temp array
                        else:
                            tempArray[placeCounter] = y[statFind+11:y.find("</span>",statFind,len(y))]
                            placeCounter = placeCounter + 1

                        statFind = y.find("stat-cell",(statFind+10),len(y))

                        #For allocating stats per team
                        if placeCounter == 9:
                            placeCounter = 0

                            #Find any data issues
                            for j in range(9):
                                if tempArray[j].find("-") > -1 or tempArray[j].find(">") > -1 or tempArray[j].find("<") > -1:
                                    tempArray[j] = tempArray[j].replace("-", "0")
                                    tempArray[j] = tempArray[j].replace(">", "0")
                                    tempArray[j] = tempArray[j].replace("<", "0")

                            statTble.append(tempArray[:])
                    addCounter = 0
                    statFind = y.find("stat-cell",x,len(y))
            for i in range(len(statTble)-confHolder):
                statTble[confHolder+i].insert(0,tbleTitles[len(tbleTitles)-1])
        else:
            looper = False

    statTble.pop(0)
    #Add team names to array
    for i in range(len(tble)):
        statTble[i].insert(0,tble[i])
        statTble[i].insert(len(statTble[i]),str(year))
    return statTble

#Inputs
    #Get current year
year = date.today().year
if date.today().month > 0 and date.today().month < 9:
    year = year - 1

    #Location input
location = input("Enter a path to where you would like to save the CSV file: ")
if location[len(location)-1] != "\\":
    location = location + "\\"

    #Date range input
toDate = input("Enter the date you would like to scrape to (x - Current Year, 2003 was the earliest): ")
if toDate.isdigit():
    toDate = int(toDate)
    if toDate < 2003 or toDate > year:
        print("Invalid year input.")
        exit()
else:
    print("Invalid year input.")
    exit()

#Pandas Dataframe
df = pd.DataFrame(columns=["Team","Conference","Conference Win","Conference Loss","Conference PF","Conference PA","Overall Win","Overall Loss","Overall PF", "Overall PA","Streak","Year"])

#Main loop through each year
while year >= toDate:
    x = scrapeESPNYear(year)
    year = year - 1
    df2 = pd.DataFrame(data=x,columns=["Team", "Conference", "Conference Win", "Conference Loss", "Conference PF", "Conference PA", "Overall Win", "Overall Loss", "Overall PF", "Overall PA", "Streak", "Year"])
    df = df.append(df2,ignore_index=True)

#Pandas
pd.set_option("display.max_colwidth",-1)
pd.set_option("display.max_rows",999)
print(df.to_string)

export_csv = df.to_csv(location + 'espnscrape.csv',index = None, header=True)
