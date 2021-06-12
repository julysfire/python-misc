import os
import time
from datetime import datetime

#Get start time for calculating total execution time
start_time = time.time()

#Try to import libraries, if not, install them
try:
    import requests
    import pandas as pd
except ImportError:
    os.system('pip install pandas')
    os.system('pip install requests')
    import requests
    import pandas as pd

def scapeESPNYear(year, league):
    #Tables
    tbleTitles = []
    tble = []
    statTble = [[]]
    tempArray = ["", "", "", "", "", "", "", "", ""]

    #Extra variables for finding text
    looper = True
    x = statFind = altFind = 1
    addCounter = placeCounter = divFinder = confHolder = 0

    #Current year has a different URL then prior seasons
    print("Year: " + str(year))
    if year == datetime.today().year-1:
        y = requests.get("https://www.espn.com/college-football/standings/_/"+league).text
    else:
        y = requests.get("https://www.espn.com/college-football/standings/_/season/"+str(year)+"/"+league).text

    #Main loop
    while looper:
        x = y.find("Table__Title", x+1, len(y))

        if x > 0:
            #Table titles
            tbleTitles.append(y[x+14:y.find("</div>", x+1, len(y))])
            x = x+20
            confHolder = len(statTble)

            #Stat-cell is for the stats, alt-find is for finding the team names
            #When altFind > statFind, end of the teams listed for the given table
            statFind = y.find("stat-cell", x, len(y))
            altFind = x

            while altFind < statFind:
                altFind = y.find("alt=", altFind, len(y))

                #Found team name
                if altFind < statFind:
                    tble.append(y[altFind+5:y.find(" title=", altFind, len(y))-1])

                    #&amp;
                    if(tble[len(tble)-1].find("amp;")) > 0:
                        tble[len(tble)-1] = tble[len(tble)-1].replace("&amp;", "&")
                    #For later to allocate stats per team
                    addCounter = addCounter + 1
                    altFind = altFind + 5
                else:
                    #Loop through the stats
                    for i in range(addCounter*7):
                        #W/L needs to be split
                        if placeCounter == 0 or placeCounter == 4:
                            midFinder = y[statFind+11:y.find("<", statFind, len(y))]
                            if midFinder == "--":
                                tempArray[placeCounter] = "0"
                                tempArray[placeCounter+1] = "0"
                            else:
                                divFinder = midFinder.find("-", 1, len(midFinder))
                                tempArray[placeCounter] = midFinder[0:divFinder]
                                tempArray[placeCounter+1] = midFinder[divFinder:len(midFinder)]
                            placeCounter = placeCounter + 2
                        #Otherwise throw it into the temp array
                        else:
                            tempArray[placeCounter] = y[statFind+11:y.find("</span>", statFind, len(y))]
                            placeCounter = placeCounter + 1

                        statFind = y.find("stat-cell", (statFind+10), len(y))

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
                    statFind = y.find("stat-cell", x, len(y))
            for i in range(len(statTble)-confHolder):
                statTble[confHolder+i].insert(0, tbleTitles[len(tbleTitles)-1])
        else:
            looper = False

    statTble.pop(0)
    #Add team names to array
    for i in range(len(tble)):
        statTble[i].insert(0, tble[i])
        statTble[i].insert(len(statTble[i]), str(year))
    return statTble


if __name__ == "__main__":
    leagues = ["", "view/fcs-i-aa", "view/d2", "view/d3"]
    for i in leagues:
        #New dataframe
        df = pd.DataFrame(columns=["Team", "Conference", "Conference Win", "Conference Loss", "Conference PF", "Conference PA", "Overall Win", "Overall Loss", "Overall PF", "Overall PA", "Streak", "Year"])

        # Get current year
        year = datetime.today().year

        #Year loop for calling data
        print("League: " + i)
        while year > 2009:
            x = scapeESPNYear(year, i)
            year = year - 1
            #Append year's data to new dataframe
            df2 = pd.DataFrame(data=x, columns=["Team", "Conference", "Conference Win", "Conference Loss", "Conference PF", "Conference PA", "Overall Win", "Overall Loss", "Overall PF", "Overall PA", "Streak", "Year"])
            #And put back in the master dataframe
            df = df.append(df2, ignore_index=True)

        #Pandas
        pd.set_option("display.max_colwidth", -1)
        pd.set_option("display.max_rows", 999)
        print(df.to_string)

        #Standardize teams
        #Many teams have changed their names so they need to be cleaned
        df["Team"] = df["Team"].str.replace('" class="Image Logo Logo__sm', "")
        df["Team"] = df["Team"].str.replace("&#x27;", "'")
        df["Team"] = df["Team"].str.replace("Florida Intl Golden Panthers", "Florida International Panthers")
        df["Team"] = df["Team"].str.replace("Mars Hill Lions", "Mars Hill Mountain Lions")
        df["Team"] = df["Team"].str.replace("Notre Dame College Blue Falcons", "Notre Dame College Falcons")
        df["Team"] = df["Team"].str.replace("Minnesota St-Moorhead Dragon", "Minnesota St-Moorhead Dragons")
        df["Team"] = df["Team"].str.replace("Bridgewater (VA) Eagles", "Bridgewater College (VA) Eagles")
        df["Team"] = df["Team"].str.replace("Bridgewater State Bears", "Bridgewater State (MA) Bears")
        df["Team"] = df["Team"].str.replace("Colby White Mules", "Colby College White Mules")
        df["Team"] = df["Team"].str.replace("Colby College Mules", "Colby College White Mules")
        df["Team"] = df["Team"].str.replace("Shenandoah Hornets", "Shenandoah University Hornets")
        df["Team"] = df["Team"].str.replace("St. Johns (MN) Johnnies", "St. John's (MN) Johnnies")
        df["Team"] = df["Team"].str.replace("St Lawrence Saints", "St. Lawrence Saints")
        df["Team"] = df["Team"].str.replace("Sul Ross State Lobos", "Sul Ross State University Lobos")
        df["Team"] = df["Team"].str.replace("Washington (MO) Bears", "Washington-Missouri Bears")
        df["Team"] = df["Team"].str.replace("Waynesburg Yellow Jackets", "Waynesburg University Yellow Jackets")
        df["Team"] = df["Team"].str.replace("San José St Spartans", "San José State Spartans")
        df["Team"] = df["Team"].str.replace("East Tennessee St. Buccaneers", "East Tennessee State Buccaneers")

        #Export to CSV
        export_csv = df.to_csv(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')+'\\espnscrape_'+i[len(i)-2:len(i)]+'.csv', index=None, header=True)

        #Drop dataframe for new scrape
        df.drop(df.index, inplace=True)
        df2.drop(df2.index, inplace=True)

#Total runtime of script
print("Execution time in seconds: " + str(time.time() - start_time))
