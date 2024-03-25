import mysql.connector

# Setup MYSQL
MYSQL_HOST = ""
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

header_id = ""
header_cyclone_num = ""
header_year = ""
header_name = ""
header_track_results = 0

def get_data():
    sql = 'INSERT INTO hurricane_data (header_id, cyclone_num_for_year, year, name, track_results, YYYYMMDD, month, day, HHMM, hour, min, record_identifier, storm_status, lat, long, max_wind_kts, min_pressure) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    sql = 'INSERT INTO hurricane_data (header_id, cyclone_num_for_year, year, name, track_results, YYYYMMDD, month, day, HHMM, hour, min, record_identifier, storm_status, lat, longs, max_wind_kts, min_pressure) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    with open(r"c:\users\userName\Downloads\hurricaneData.txt", "r") as filestream:
        for line in filestream:
            #Strip newline
            line = line[:len(line)-1]
            zz = []

            #Header row
            if line[0:2] == "AL":
                comma = line.find(",")
                header_id = line[:comma]
                header_cyclone_num = header_id[2:len(header_id)-4]
                header_year = int(header_id[len(header_id)-4:])

                comma2 = line.find(",", comma+1)
                header_name = line[comma+1:comma2].strip()

                comma = line.find(",", comma2+1)
                header_track_results = int(line[comma2+1:comma].strip())
            else:
                #Header stuff
                zz.append(header_id)
                zz.append(header_cyclone_num)
                zz.append(header_year)
                zz.append(header_name)
                zz.append(header_track_results)

                #Body
                comma = line.find(",")
                YYYYMMDD = line[:comma]
                zz.append(YYYYMMDD) #YYYYMMDD
                zz.append(int(YYYYMMDD[4:6])) #Month
                zz.append(int(YYYYMMDD[6:])) #Day

                comma2 = line.find(",", comma + 1)
                HHMM = line[comma+1:comma2].strip()
                zz.append(HHMM)  #HHMM
                zz.append(int(HHMM[0:2])) #HH
                zz.append(int(HHMM[2:4])) #MM

                comma = line.find(",", comma2 + 1)
                zz.append(line[comma2+1:comma].strip()) #Identifier

                comma2 = line.find(",", comma + 1)
                zz.append(line[comma+1:comma2].strip()) #Storm Status

                comma = line.find(",", comma2 + 1)
                zz.append(line[comma2 + 1:comma].strip())  #LAT

                comma2 = line.find(",", comma + 1)
                zz.append(line[comma + 1:comma2].strip())  #LONG

                comma = line.find(",", comma2 + 1)
                zz.append(line[comma2 + 1:comma].strip())  #Max Wind Kts

                comma2 = line.find(",", comma + 1)
                zz.append(line[comma + 1:comma2].strip())  #Min Pressure

                insertVals = (zz[0], zz[1], zz[2], zz[3], zz[4], zz[5], zz[6], zz[7], zz[8], zz[9], zz[10], zz[11], zz[12], zz[13], zz[14], zz[15], zz[16])
                #Insert data
                mycursor.execute(sql, insertVals)

                #Commit to DB
                mydb.commit()
    print("Data Inserted.")

if __name__ == '__main__':
    get_data()
