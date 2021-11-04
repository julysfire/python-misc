import requests
from bs4 import BeautifulSoup

#Get HTML of webpage in string
url = "https://oldschool.runescape.wiki/w/Music#Track_list"
y = requests.get(url)

#Pass into the BeautifulSoup to get all tables.  All information needed on this page is found in tbales
soup = BeautifulSoup(y.text, features="html.parser")
tables = soup.findAll("table")

#Save to text file
file = open("musictracks.txt","a")

#Loop through tables
for i in tables:
    #Look for only the wikitables which contain the data needed
    if "wikitable" in i["class"]:
        rows = i.findChildren("tr")

        for j in rows:
            #Get text for entire row
            rowText = j.text
            #Replace new line characters with underscore and then split on that for array
            rowText = rowText.replace("\n", "_")
            rowArray = rowText.split("_")
            #Trim extra array elements that are not needed
            rowArray = rowArray[1:-7]
            rowArray.pop(1)

            #Final result
            if rowArray[0] != "Name":
                file.writelines(rowArray[0] + " - " + rowArray[1] + "\n")
                print(rowArray)
file.close()
