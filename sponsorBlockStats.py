#
#Required: publicUserId          This is your public user ID from SponsorBlock.
#Required: fileSaveLocation      This is the location where you would like to save your CSV.
#
#Example: python sponsorBlockSats.py "publicUserId", "fileSaveLocation"
#         python sponsorBlockStats.py "1234567890asdfghjkl", "C:\Users\JoeSmo\Desktop\"
#

#Writing to CSV
import csv

#OS for install requests if needed, sys for arguments, datetime for logging time to CSV
import os
import sys
from datetime import datetime

#Check if requests is installed, if not, install it and import
try:
    import requests
except ImportError:
    os.system('pip install requests')
    import requests

#Check arguments
if len(sys.argv) < 2:
    print("Missing argument.  Please provide the following 2 arguments when running this file: publicUserId saveLocation")
    exit()

#Get info from userStats
params = {"publicUserID": sys.argv[1]}
y = requests.get("https://sponsor.ajay.app/api/userInfo", params=params).json()

#Get category information
params = {"publicUserID": sys.argv[1], "fetchCategoryStats": "true"}
x = requests.get("https://sponsor.ajay.app/api/userStats", params=params).json()
x = x['categoryCount'] #For easy access to the categories

#Get all data together for writing to CSV
statData = [datetime.now().strftime("%m/%d/%Y %H:%M:%S"), y['minutesSaved'], y['segmentCount'], y['ignoredSegmentCount'], y['viewCount'], y['ignoredViewCount'], y['warnings'], y['reputation'],
            x['sponsor'], x['intro'], x['outro'], x['interaction'], x['selfpromo'], x['music_offtopic'], x['preview'], x['poi_highlight'], x['filler'], x['exclusive_access']]

#Check if file exists, if not, create one and write headers
filePath = (sys.argv[2] + "sponorBlockStats.csv").replace('"', "\\")

if os.path.exists(filePath):
    f = open(filePath, 'a', newline='')
    writer = csv.writer(f)
else:
    #Save to CSV
    f = open(filePath, 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(['Date/Time', 'Minutes Saved', 'Segment Count', 'Ignored Segment Count', 'View Count', 'Ignored View Count', 'Warnings', 'Reputation',
                     'Sponsor Segments', 'Intro Segments', 'Outro Segments', 'Interaction Segments', 'Selfpromo Segments', 'Music-Offtopic Segments', 'Preview Segments', 'POI Segments', 'Filler Segments', 'Exclusive Access Segments'])

writer.writerow(statData)
f.close()

print("Data saved to CSV.")
print(statData)
