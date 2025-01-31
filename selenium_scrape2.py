import time
import random
import os
import shutil
from datetime import datetime

#Selenium setup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
opts = Options()
opts.headless = True
browser = Firefox(options=opts)

firstRun = True

def getNOAAMessage():
    browser.get("https://www.nhc.noaa.gov/gtwo.php?basin=atlc&fdays=7")

    randNumNOAA = random.randint(1, 3)
    time.sleep(randNumNOAA)

    textField = browser.find_element(By.CLASS_NAME, "textproduct")
    print(textField.text)


while True:
    #Navigate to page and click button
    browser.get("https://www.weather_site_here.com/analysis/models/?model=gfs&region=atl&pkg=mslp_pcpn")
    print("Opened URL.")

    randNum = random.randint(1, 3)
    time.sleep(randNum)

    #Get through Intro
    if firstRun:
        skipButt = browser.find_element(By.CLASS_NAME, "introjs-skipbutton")
        skipButt.click()
        print("Skipped tutorial.")
        firstRun = False

    randNum = random.randint(1, 3)
    time.sleep(randNum)

    #Request Forecast GIF
    forcastButt = browser.find_element(By.ID, "fcstGIF-button")
    forcastButt.click()

    #Set parameters
    endingHour = browser.find_element(By.ID, "fcstGIF-FH2")
    endingHour.send_keys("384")

    fps = browser.find_element(By.ID, "fcstGIF-fps")
    fps.clear()
    fps.send_keys("5")

    submitButt = browser.find_element(By.ID, "fcstGIF-submit")
    submitButt.click()
    print("Requested forecast GIF.")

    time.sleep(10)

    #Rename file and move
    currentYYYYMM = datetime.today().strftime('%Y%m%d')
    currentRun = int(datetime.now().strftime("%H"))
    if 0 < currentRun < 6:
        currentRun = "000"
    elif 6 < currentRun < 12:
        currentRun = "600"
    elif 12 < currentRun < 18:
        currentRun = "1200"
    else:
        currentRun = "1800"

    try:
        os.rename("C:\\Users\\user_name_here\\Downloads\\gfs_mslp_pcpn_atl_fh6-384.gif", "C:\\Users\\user_name_here\\Downloads\\" + currentYYYYMM + "_" + currentRun + "_GFS_model.gif")
        print("Renamed file.")

        shutil.move("C:\\Users\\user_name_here\\Downloads\\" + currentYYYYMM + "_" + currentRun + "_GFS_model.gif", "H:\\Documents\\GFS Models\\" + currentYYYYMM + "_" + currentRun + "_GFS_model.gif")
        print("Moved file.")
        print("")
    except Exception:
        print("Didn't find file.  This is most likely due to a new file being generated.")

    getNOAAMessage()

    print("-------------------")

    #Sleep until next run is ready
    curTime = datetime.now()

    if 8 <= curTime.hour < 14:
        sleepUntil = datetime.now().replace(hour=14, minute=0, second=0)
    elif 14 <= curTime.hour < 20:
        sleepUntil = datetime.now().replace(hour=20, minute=0, second=0)
    elif 0 <= curTime.hour < 8:
        sleepUntil = datetime.now().replace(hour=8, minute=0, second=0)
    else:
        sleepUntil = datetime.now().replace(hour=2, minute=0, second=0)

    sec = (sleepUntil - curTime).seconds

    #TEST
    #sec = 15

    print("Sleeping for " + str(sec) + " seconds until : " + str(sleepUntil))
    time.sleep(sec)
    browser.refresh()
