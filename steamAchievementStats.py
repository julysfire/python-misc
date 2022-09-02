import requests
import mysql.connector
import json

#Variables
MYSQL_HOST = ""  #Where your db is hosted
MYSQL_USER = ""  #DB user
MYSQL_PASSWORD = "" #DB user password
MYSQL_DATABASE_NAME = "" #DB name
STEAM_API_KEY = ""   #https://partner.steamgames.com/doc/webapi_overview/auth
STEAM_PROFILE_ID = ""               #https://www.steamidfinder.com/
U_ID_NAME = ""  #Username on Steam


# Setup MySQL connection and query
mydb = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE_NAME
)
mycursor = mydb.cursor()


def getAppListDB(tableName):
    mycursor.execute("TRUNCATE TABLE " + tableName)
    mydb.commit()

    sql = "INSERT INTO " + tableName + " (app_name, appid) VALUES (%s, %s)"

    #Get list of all apps
    response = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/').text
    responseData = json.loads(response)
    responseData = responseData["applist"]["apps"]

    #Loop through apps and insert to DB
    for app in responseData:
        appval = (app["name"], app["appid"])
        mycursor.execute(sql, appval)

    #Commit to DB
    mydb.commit()
    print("Records inserted.")


def getOwnedGames(tableName):
    mycursor.execute("TRUNCATE TABLE " + tableName)
    mydb.commit()

    sql = "INSERT INTO " + tableName + " (game_name,appid,achievements) VALUES (%s, %s, %s)"

    #Get list of all games
    response = requests.get("https://steamcommunity.com/id/"+ U_ID_NAME + "/games/?tab=all").text
    response = response[response.find('var rgGames')+14:response.find('var rgChangingGames')-5]
    responseData = json.loads(response)

    #Loop through apps and insert to DB
    for app in responseData:
        appval = (app["name"], app["appid"], 1 if app["availStatLinks"]["achievements"] else 0)
        mycursor.execute(sql, appval)

    #Commit to DB
    mydb.commit()
    print("Records inserted.")


def getAllAchievements(tableName, ownedGamesTable):
    mycursor.execute("TRUNCATE TABLE " + tableName)
    mydb.commit()

    # Get a list of all games with achievements
    mycursor.execute("SELECT game_name, appid FROM " + ownedGamesTable + " WHERE achievements = 1")
    achievementGames = mycursor.fetchall()

    sql = "INSERT INTO " + tableName + " (game_name,achievement_id,achievement_status) VALUES (%s, %s, %s)"

    #Scrape the xml to get a list of all achievements
    for game in achievementGames:
        url = 'https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/?key='+STEAM_API_KEY+'&steamid='+STEAM_PROFILE_ID+'&appid=' + str(game[1])
        response = requests.get(url).text
        responseData = json.loads(response)
        try:
            for achieve in responseData["playerstats"]["achievements"]:
                achieveval = (game[0], achieve["apiname"], achieve["achieved"])
                mycursor.execute(sql, achieveval)
        except KeyError:
            print(game[0] + " doesn't have achievements.")

    #Commit to DB
    mydb.commit()
    print("Records inserted.")


def getAchievementListDB(tableName, ownedGamesTable):
    mycursor.execute("TRUNCATE TABLE " + tableName)
    mydb.commit()

    sql = "INSERT INTO " + tableName + " (game_name,achievement_name,achievement_id,description,hidden,default_value) VALUES (%s, %s, %s, %s, %s, %s)"

    # Get a list of all games with achievements
    mycursor.execute("SELECT game_name, appid FROM " + ownedGamesTable + " WHERE achievements = 1")
    achievementGames = mycursor.fetchall()

    #Scrape the xml to get a list of all achievements
    for game in achievementGames:
        url = "https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key="+STEAM_API_KEY+"&appid=" + str(game[1])
        response = requests.get(url).text
        responseData = json.loads(response)
        try:
            for achieve in responseData["game"]["availableGameStats"]["achievements"]:
                try:
                    description = achieve["description"]
                except KeyError:
                    description = ""
                achieveval = (game[0], achieve["displayName"], achieve["name"], description, achieve["hidden"], achieve["defaultvalue"])
                mycursor.execute(sql, achieveval)
        except KeyError:
            print(game[0] + " doesn't have achievements.")

    #Commit to DB
    mydb.commit()
    print("Records inserted.")


def getAchievementPercentages(tableName, ownedGamesTable):
    mycursor.execute("TRUNCATE TABLE " + tableName)
    mydb.commit()

    sql = "INSERT INTO " + tableName + " (game_name,achievement_id,achievement_percentage) VALUES (%s, %s, %s)"

    # Get a list of all games with achievements
    mycursor.execute("SELECT game_name, appid FROM " + ownedGamesTable + " WHERE achievements = 1")
    achievementGames = mycursor.fetchall()

    #Scrape the xml to get a list of all achievements
    for game in achievementGames:
        url = "https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2/?gameid=" + str(game[1])
        response = requests.get(url).text
        responseData = json.loads(response)
        try:
            for achieve in responseData["achievementpercentages"]["achievements"]:
                achieveval = (game[0], achieve["name"], achieve["percent"])
                mycursor.execute(sql, achieveval)
        except KeyError:
            print(game[0] + " doesn't have achievements.")

    #Commit to DB
    mydb.commit()
    print("Records inserted.")


if __name__ == '__main__':
    #Builds a table of all steam items and their appid.
    #getAppListDB("steamapps")

    #Get a list of all owned games
    #getOwnedGames("steamownedgames")

    #Get a list of all achievements
    getAllAchievements("steamachievements", "steamownedgames")

    #Get a full list of achievements and their names/descriptions
    getAchievementListDB("steamachievementsdetails", "steamownedgames")

    #Get a full list of the global achievement percentages
    getAchievementPercentages("achivements_global_percentage", "steamownedgames")
