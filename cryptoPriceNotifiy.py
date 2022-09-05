import datetime
import json
import time
import requests
from win10toast import ToastNotifier

firstTimeRunFlag = True

#Infinite loop
while True:
    #Get JSON exchange rates from Coinbase
    url = "https://api.coinbase.com/v2/exchange-rates?currency=USD"
    response = requests.get(url).text
    jsonData = json.loads(response)
    jsonData = jsonData["data"]["rates"]

    #Get rates
    btcRate = format(float(1/float(jsonData["BTC"])), '.5f')
    batRate = format(float(1/float(jsonData["BAT"])), '.8f')
    dogeRate = format(float(1/float(jsonData["DOGE"])), '.8f')

    #If it is the first time running, set these to current prices for 0.00% change, otherwise div0 error
    if firstTimeRunFlag:
        btcOld = btcRate
        batOld = batRate
        dogeOld = dogeRate
        firstTimeRunFlag = False

    #Calculate percent change in prices
    btcPercChg = format(((float(btcRate)-float(btcOld))/float(btcRate))*100, '.2f')
    batPercChg = format(((float(batRate)-float(batOld))/float(batRate))*100, '.2f')
    dogePercChg = format(((float(dogeRate)-float(dogeOld))/float(dogeRate))*100, '.2f')

    #Windows notification
    toast = ToastNotifier()
    toastText = "\nBTC: {}  Change: {}%\nBAT: {}  Change: {}%\nDOGE: {}  Change: {}%".format(btcRate, btcPercChg, batRate, batPercChg, dogeRate, dogePercChg)
    toast.show_toast("Crypto Prices As of " + (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime("%H:%M"), toastText, duration=10)

    #Set old rates to current for calculating percent change
    btcOld = btcRate
    batOld = batRate
    dogeOld = dogeRate
    
    #Sleep until next top of the hour
    curTime = datetime.datetime.now()
    sleepUntil = curTime + datetime.timedelta(hours=1)
    sleepUntil = sleepUntil.replace(minute=0, second=0, microsecond=0)

    sec = (sleepUntil - curTime).seconds
    time.sleep(sec)
