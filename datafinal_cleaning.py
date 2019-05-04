import os
from bs4 import BeautifulSoup as bs
import numpy as np
import pandas as pd
import requests
import json
import csv
import xlrd
import time
import datetime

folder = "E:/data_analytics_1/data_project/manager_log"
openFolder = os.listdir(folder)
csv_folder = "E:/data_analytics_1/data_project/log_folder"


def csv_convert(x):
    filePre = ("/" + str(x))
    filepath = (str(folder) + str(filePre))
    file = xlrd.open_workbook(filepath)
    sheet = file.sheet_by_name('Sheet1')
    newFileName = (str(filePre.strip(".xlsx")) + ".csv")
    newPath = (str(csv_folder) + str(newFileName))
    csv_file = open(newPath, 'w')
    write = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sheet.nrows):
        write.writerow(sheet.row_values(rownum))

    csv_file.close()

for f in openFolder:
    csv_convert(f)

#############################################################
folder = "E:/data_analytics_1/data_project/log_folder"
openFolder = os.listdir(folder)
headerList = ["date", "day", "net", "alcohol", "food", "weather"]
writeList = []
 #work on this to write data to new csv file!!!

def clean(x):
    filepath = (str(folder)+ "/" + str(x))
    file = open(filepath, "r")
    reader = csv.reader(file)
    rows = list(reader)
    fileDate = (str(x)).strip(".csv")
    date = fileDate.replace("-", ".")
    inputList = []
    day = rows[4][1]
    net = rows[16][1]
    alcohol = rows[12][1]
    food = rows[14][1]
    weather = rows[6][1]


    if date[0] != "0" and date[1] == ".":
        date = ("0" + str(date))
    if date[3] != "0" and date[5] != ".":
        date = str(date[0:3]) + "0" + str(date[3:])
    if date[-3] == ".":
        delim1 = date[-2]
        delim2 = date[-1]
        date = (str(date[0:6]) + "20" + str(delim1) + str(delim2))
    if day[0:2] == "Mo":
        day = "Monday"
    elif day[0:2] == "Tu":
        day = "Tuesday"
    elif day[0:2] == "We":
        day = "Wednesday"
    elif day[0:2] == "Th":
        day = "Thursday"
    elif day[0:2] == "Fr":
        day = "Friday"
    elif day[0:2] == "Sa" or day[0:2] == "sa":
        day = "Saturday"
    elif day[0:2] == "Su":
        day = "Sunday"

    inputList.append(date)
    inputList.append(day)
    inputList.append(net)
    inputList.append(alcohol)
    inputList.append(food)
    inputList.append(weather)

    writeList.append(inputList)


for i in openFolder:
    clean(i)

with open("E:/data_analytics_1/data_project/spreadsheet.csv", "w+") as spreadsheet:
    writer = csv.DictWriter(spreadsheet, fieldnames=headerList)
    writer.writeheader()

    for w in writeList:
        writer.writerow({"date":w[0],
                            "day":w[1],
                            "net":w[2],
                            "alcohol":w[3],
                            "food":w[4],
                            "weather":w[5]})
#################################################################
stLatLong = "40.4462007,-80.0125109"


with open("E:/data_analytics_1/data_project/spreadsheet.csv", "r") as spreadsheet:
    reader = csv.reader(spreadsheet)
    obv = [row for row in reader]
    headerList = obv[0]
    writeList = []

    for row in obv:
        inputList = []
        date = row[0]
        day = row[1]
        net = row[2]
        alcohol = row[3]
        food = row[4]
        avg_temp = row[5]
        weather_icon = row[6]
        steelers = row[7]
        pirates = row[8]
        penguins = row[9]
        panthers = row[10]
        stage_ae = row[11]

        if steelers != "1":
            steelers = "0"
        if pirates != "1":
            pirates = "0"
        if penguins != "1":
            penguins = "0"
        if panthers != "1":
            panthers = "0"
        if stage_ae != "1":
            stage_ae = "0"

        d = [i for i in date]
        if d[0] != "d":
            month = d[0] + d[1]
            dayDay = d[3] + d[4]
            year = d[6] + d[7] + d[8] + d[9]
            dateInsert = (str(year) + "-" + str(month) + "-" + str(dayDay))
            timestamp = time.mktime(datetime.datetime.strptime(dateInsert, "%Y-%m-%d").timetuple())
            newStamp = int(timestamp)
            darkSkyURL = ("https://api.darksky.net/forecast/" + str(dsAPIKEY) + "/" + str(stLatLong) + "," + str(newStamp) + "?exclude=hourly,flags")
            dsAPI = requests.get(darkSkyURL)
            dsJSON = json.loads(dsAPI.text)
            weather = dsJSON['daily']['data'][0]
            weatherIcon = weather['icon']
            tempLow = weather['temperatureHigh']
            tempHigh = weather['temperatureLow']
            avgTemp = round(((float(tempHigh) + float(tempLow)) / 2), 2)
            avg_temp = avgTemp
            weather_icon = weatherIcon



            inputList.append(date)
            inputList.append(day)
            inputList.append(net)
            inputList.append(alcohol)
            inputList.append(food)
            inputList.append(avg_temp)
            inputList.append(weather_icon)
            inputList.append(steelers)
            inputList.append(pirates)
            inputList.append(penguins)
            inputList.append(panthers)
            inputList.append(stage_ae)


            writeList.append(inputList)


    with open("E:/data_analytics_1/data_project/new_spreadsheet.csv", 'w+') as newFile:
        writer = csv.DictWriter(newFile, fieldnames=headerList)
        writer.writeheader()

        for w in writeList:
            writer.writerow({"date": w[0],
                             "day": w[1],
                             "net": w[2],
                             "alcohol": w[3],
                             "food": w[4],
                             "avg_temp": w[5],
                             "weather_icon": w[6],
                             "steelers": w[7],
                             "pirates": w[8],
                             "penguins": w[9],
                             "panthers": w[10],
                             "stage_ae": w[11]})

