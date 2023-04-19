import json
import requests
import mysql.connector
import datetime
from datetime import date
import smtplib
from email.mime.text import MIMEText

# Setup MYSQL
MYSQL_HOST = "localhost"
MYSQL_USER = ""
MYSQL_PASSWORD = ""
MYSQL_DATABASE_NAME = ""

mydb = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE_NAME
)
mycursor = mydb.cursor()


def getData():
    # Setup request to RapidAPI and get response
    url = ""
    querystring = {"url": ""}
    headers = {
        "X-RapidAPI-Key": "",
        "X-RapidAPI-Host": ""
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    responseJson = json.loads(response.text)


    for i in responseJson["results"]:
        sql = "INSERT INTO properties (bathrooms, bedrooms, city, country, currency, datePriceChanged, daysOnZillow, homeStatus, homeStatusForHDP, homeType, isFeatured, isNonOwnerOccupied, isPreforeclosureAuction, isPremierBuilder, isUnmappable, isZillowOwned, latitude, longitude, latLongCombined, is_newHome, is_FSBA, livingArea, lotAreaUnit, lotAreaValue, newConstructionType, price, priceChange, percentChange, priceForHDP, priceReduction, rentZestimate, shouldHighlight, state, streetAddress, taxAssessedValue, zestimate, zipcode, zpid, url, fullAddress, snapshotDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        vals = ["bathrooms", "bedrooms", "city", "country", "currency", "datePriceChanged", "daysOnZillow", "homeStatus", "homeStatusForHDP", "homeType", "isFeatured", "isNonOwnerOccupied", "isPreforeclosureAuction", "isPremierBuilder", "isUnmappable", "isZillowOwned", "latitude", "longitude", "latLongCombined", "is_newHome", "is_FSBA", "livingArea", "lotAreaUnit", "lotAreaValue", "newConstructionType", "price", "priceChange", "percentChange", "priceForHDP", "priceReduction", "rentZestimate", "shouldHighlight", "state", "streetAddress", "taxAssessedValue", "zestimate", "zipcode", "zpid", "url", "fullAddress", "snapshotDate"]
        z = []

        #Get all the values ready
        for v in vals:
            try:
                if v == "is_newHome" or v == "is_FSBA":
                    newObj = i["listing_sub_type"]
                    z.append(newObj[v])
                elif v == "snapshotDate":
                    z.append(str(date.today()))
                elif v == "url":
                    z.append("zillow.com/homedetails/" + str(i["zpid"]) + "_zpid/")
                elif v == "datePriceChanged":
                    z.append(str(datetime.datetime.fromtimestamp(i["datePriceChanged"] / 1000)))
                elif v == "latLongCombined":
                    z.append("(" + str(i["latitude"]) + ", " + str(i["longitude"]) + ")")
                elif v == "percentChange":
                    if int(i["priceChange"]) < 0:
                        orig = int(i["price"]) + int(abs(i["priceChange"]))
                        negFlag = True
                    else:
                        orig = int(i["price"]) - int(abs(i["priceChange"]))
                        negFlag = False

                    numerator = abs(orig - int(i["price"]))
                    denom = (orig + int(i["price"])) / 2

                    percentChg = str(round((numerator / denom) * 100, 4)) + "%"
                    z.append(("-" if negFlag else "") + percentChg)
                elif v == "fullAddress":
                    z.append(i["streetAddress"] + " " + i["city"] + ", " + i["state"] + " " + i["zipcode"])
                else:
                    z.append(i[v])
            except KeyError:
                z.append(None)

        #Final prepare SQL and execute
        insertVals = (z[0], z[1], z[2], z[3], z[4], z[5], z[6], z[7], z[8], z[9], z[10], z[11], z[12], z[13], z[14], z[15], z[16], z[17], z[18], z[19], z[20], z[21], z[22], z[23], z[24], z[25], z[26], z[27], z[28], z[29], z[30], z[31], z[32], z[33], z[34], z[35], z[36], z[37], z[38], z[39], z[40])
        mycursor.execute(sql, insertVals)

        #Commit to DB
        mydb.commit()
    print("Records inserted.")

def analysisReport():
    analysisReportData = " ----- ANALYSIS FOR " + str(date.today()) + " -----\n---Percent with Reductions---\nDate                Percent\n"
    #Percent of homes with price decreases
    SQL = "select p.snapshotDate, (rc.totalCount / dx.totalCount) * 100 as percentReduced from zillow_data.properties p left join (select count(*) as totalCount, snapshotDate from zillow_data.properties group by snapshotDate) dx on dx.snapshotDate = p.snapshotDate left join (select count(*) as totalCount, snapshotDate from zillow_data.properties where datePriceChanged is not null group by snapshotDate) rc on rc.snapshotDate = p.snapshotDate group by p.snapshotDate order by 1;"
    mycursor.execute(SQL)

    myresults = mycursor.fetchall()
    for i in myresults:
        analysisReportData = analysisReportData + str(i[0]) + "        " + str(i[1]) + "\n"

    #New Price Drops
    analysisReportData = analysisReportData + "\n\n--- New Price Drops ---\nAddress                                     URL                                           Price         Price Change     Percent Change          Bedrooms          Living Area\n"
    SQL = "select p.fullAddress, p.url, p.price, p.priceChange, p.percentChange, p.bedrooms, p.livingArea from zillow_data.properties p left join (select latLongCombined, price from zillow_data.properties where snapshotDate = CURDATE() -1) pd on pd.latLongCombined = p.latLongCombined where snapshotDate = CURDATE() and pd.price > p.price;"
    mycursor.execute(SQL)

    myresults = mycursor.fetchall()
    for i in myresults:
        analysisReportData = analysisReportData + i[0] + "        " + i[1] + "        " + str(i[2]) + "        " + str(i[3]) + "           " + str(i[4]) + "                " + str(i[5]) + "                 " + str(i[6]) + "\n"

    #New Listings
    analysisReportData = analysisReportData + "\n\n--- New Listings Today ---\nAddress                                                           URL                                                                 Price        Bedrooms  Bathrooms   Living Area (sqft)          Lat, Long                               Is New Home?          Lot Area        Lot Area Units\n"
    SQL = "select p.fullAddress, p.url, p.price, p.bedrooms, p.bathrooms, p.livingArea, p.latLongCombined, p.is_newHome, p.lotAreaValue, p.lotAreaUnit from zillow_data.properties p where p.latLongCombined not in (select distinct latLongCombined from zillow_data.properties where snapshotDate = CURDATE() -1) and snapshotDate = CURDATE();"
    mycursor.execute(SQL)

    myresults = mycursor.fetchall()
    for i in myresults:
        analysisReportData = analysisReportData + i[0] + "         " + i[1] + "         " + str(i[2]) + "      " + str(i[3]) + "                " + str(i[4]) + "                 " + str(i[5]) + "                             " + str(i[6]) + "           " + str(i[7]) + "                        " + str(i[8]) + "                 " + str(i[9]) + "\n"

    #Delistings
    analysisReportData = analysisReportData + "\n\n--- Delistings Today ---\nAddress                                                             URL                                                                 Price        Bedrooms  Bathrooms   Living Area (sqft)          Lat, Long                               Is New Home?          Lot Area        Lot Area Units\n"
    SQL = "select p.fullAddress, p.url, p.price, p.bedrooms, p.bathrooms, p.livingArea, p.latLongCombined, p.is_newHome, p.lotAreaValue, p.lotAreaUnit from zillow_data.properties p where p.latLongCombined not in (select distinct latLongCombined from zillow_data.properties where snapshotDate = CURDATE()) and snapshotDate = CURDATE() -1;"
    mycursor.execute(SQL)

    myresults = mycursor.fetchall()
    for i in myresults:
        analysisReportData = analysisReportData + i[0] + "         " + i[1] + "         " + str(i[2]) + "      " + str(i[3]) + "                " + str(i[4]) + "                 " + str(i[5]) + "                             " + str(i[6]) + "           " + str(i[7]) + "                        " + str(i[8]) + "                 " + str(i[9]) + "\n"

    #Average Price Per Bedroom
    analysisReportData = analysisReportData + "\n\n--- Average Price By Bedroom ---\nDate           Bedrooms        Average Price\n"
    SQL = "select snapshotDate, bedrooms, avg(price) from zillow_data.properties group by snapshotDate, bedrooms order by 1;"
    mycursor.execute(SQL)

    myresults = mycursor.fetchall()
    for i in myresults:
        analysisReportData = analysisReportData + str(i[0]) + "         " + str(i[1]) + "         " + str(i[2]) + "\n"

    #Price Per Sqft By Date
    analysisReportData = analysisReportData + "\n\n--- Price Per sqft By Date ---\nDate                  Price Per Sqft\n"
    SQL = "select p.snapshotDate, avg(p.price / p.livingArea) as pricePerSqFt from zillow_data.properties p group by snapshotDate order by 1;"
    mycursor.execute(SQL)

    myresults = mycursor.fetchall()
    for i in myresults:
        analysisReportData = analysisReportData + str(i[0]) + "         " + str(i[1]) + "\n"

    print(analysisReportData)
    return analysisReportData

def sendEmail(reportData):
    sender = ""
    receiver = ""
    message = MIMEText(reportData)
    message['Subject'] = 'Daily Report for ' + str(date.today())
    message['From'] = sender
    message['To'] = receiver

    server = smtplib.SMTP_SSL('smtp.comcast.net', port=465)
    server.login(sender, "")
    server.sendmail(sender, receiver, message.as_string())
    server.quit()
    print("Email sent")


if __name__ == '__main__':
    getData()
    report = analysisReport()
    sendEmail(report)
