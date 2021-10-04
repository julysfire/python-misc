import requests
import json

#Custom header otherwise blocked
headers = {
    'User-Agent': 'Testing, learning JSON and API, seeing what I can make - Julysfire#9465'
}

#Mapping data
mappingUrl = "https://prices.runescape.wiki/api/v1/osrs/mapping"
response = requests.get(mappingUrl, headers=headers).text
mappingData = json.loads(response)

#Latest prices
pricesUrl = "https://prices.runescape.wiki/api/v1/osrs/latest"
response = requests.get(pricesUrl, headers=headers).text
pricesData = json.loads(response)
pricesData = pricesData["data"]


#High Alch profit
xAlch = []
for i in mappingData:
    #Get GE price, pass if it isn't found in latest prices files
    try:
        itemInfo = pricesData[str(i["id"])]
        gePrice = itemInfo["high"] + 207   #207 is roughly the price of a nature rune

        #Profit to high alch
        if gePrice < i["highalch"]:
            xAlch.append([i["name"],i["limit"],gePrice,i["highalch"], i["highalch"]-gePrice])
    except KeyError:
        pass

xAlch = sorted(xAlch, key=lambda x: x[4], reverse=True)
xAlch.insert(0,["Item Name", "Limit", "Buy Price", "Alch Amount", "Alch Profit"])
for i in xAlch:
    print(i)
