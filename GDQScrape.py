import os
from datetime import datetime

#Get packages
try:
    import requests
    import pandas as pd
except ImportError:
    os.system('pip install pandas')
    os.system('pip install requests')
    import requests
    import pandas as pd

def scrapeFunction(page, year, event):
    print("Page: " + str(page))
    # Variables
    pageTable = [[]]
    looper, donoLooper = True, True

    #Get html
    y = requests.get('https://gamesdonequick.com/tracker/donations/'+event+year+'?page='+str(page)).text

    #Initial trim
    xbeg = y.find('class="dsc"><span style="display:none;">Dsc</span></a>', 0, len(y))
    xend = y.find('<p class="text-center larger">', xbeg, len(y))
    y = y[xbeg:xend]

    #Loop through all donos
    while donoLooper:
        donoArray = []
        if y.find('<tr class="">', 0, len(y)) > -1:
            xDono = y.find('<tr class="">', 0, len(y))
            yDono = y[xDono:y.find('<tr class="">', xDono+14)]

            #Name
            if yDono.find("/tracker/donor/", 0, len(yDono)) > 0:
                xName = yDono.find("/tracker/donor/", 0, len(yDono))
                xName = yDono.find(">", xName, len(yDono))
                stringName = yDono[xName+2:yDono.find("<", xName, len(yDono))-1]
                stringName = stringName.replace(",", ";")
                stringName = stringName.strip()
                donoArray.append(stringName)
            else:
                donoArray.append("Anonymous")

            #Date and Time
            xTime = yDono.find('<td class="datetime">', 0, len(yDono)) + 21
            time = yDono[xTime+1:yDono.find("<", xTime, len(yDono))-1]
            #Date
            date = time[0:time.find('T', 0, len(time))]
            date = date.strip()
            donoArray.append(date)

            #Time
            time = time[time.find('T', 0, len(time))+1:time.find('.', 0, len(time))]
            if time.find("-") > 0:
                time = time[:time.find("-")]
            donoArray.append(time)

            #Dono Amount
            xAmt = yDono.find('<a href="/tracker/donation/', 0, len(yDono)) + 28
            xAmt = yDono.find(">", xAmt, len(yDono))
            donoString = yDono[xAmt+1:yDono.find("<", xAmt, len(yDono))]
            donoString = donoString.replace("$","")
            donoString = donoString.replace(",","")
            donoArray.append(float(donoString))

            #Comment?
            xCmt = yDono.find('<td>', xAmt, len(yDono)) + 5
            xCmtEnd = yDono.find('</td>', xCmt, len(yDono)) - 1
            donoArray.append(yDono[xCmt:xCmtEnd])

            #Append to table
            pageTable.append(donoArray)
            y = y[y.find('<tr class="">', xDono+14):len(y)]
        else:
            donoLooper = False
    pageTable.pop(0)
    return pageTable


#Main function
if __name__ == "__main__":
    #Event and year input
    eventIn = input("Which event would you like to scrape? (AGDQ or SGDQ) ").lower()
    yearIn = input("Which year would you like to scrape? (2011 - Current) ")

    if eventIn != "agdq" and eventIn != "sgdq":
        print("Please only enter AGDQ or SGDQ.")
        exit()

    if int(yearIn) < 2011 or int(yearIn) > datetime.now().year:
        print("Bad year input.")
        exit()

    # Location input
    location = input("Enter a path to where you would like to save the CSV file: ")
    if location[len(location) - 1] != "\\":
        location = location + "\\"
    if not os.path.isdir(location):
        print("Path entered does not exist.")
        exit()

    # Variables
    # Dataframe
    df = pd.DataFrame(columns=["Name", "Date", "Time", "Amount", "Comment"])

    pageCounter = 1

    # Get total pages
    y = requests.get('https://gamesdonequick.com/tracker/donations/'+eventIn+yearIn).text
    totalPages = y.find('<label for="sort">of')
    totalPages = y[totalPages+21:y.find("<", totalPages+1, len(y))]

    print("Total Pages: " + str(totalPages))

    # Main Loop
    while pageCounter < int(totalPages):
        x = scrapeFunction(pageCounter, yearIn, eventIn)
        df2 = pd.DataFrame(data=x, columns=["Name", "Date", "Time", "Amount", "Comment"])
        df = df.append(df2, ignore_index=True)

        pageCounter = pageCounter + 1

    # Save out
    print(df.to_string)
    export_csv = df.to_csv(location + eventIn + yearIn + ".csv", index=None, header=True)
