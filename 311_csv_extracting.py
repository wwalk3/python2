import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

dataFile = open("C:/Users/wwalk_000/desktop/311_data.csv")
reader = csv.DictReader(dataFile)

requests = []
totalRequests = []
neighborhoods = []
totalNeighborhoods = []
hoodIndex = []
requestIndex = []

for row in reader:                                       #takes information in from the csv
    totalRequests.append(row['REQUEST_TYPE'])
    totalNeighborhoods.append(row['NEIGHBORHOOD'])


def makeAList(x, y, z):            #makes the data easier to operate on
    index = 0
    for item in x:
        if item not in y:
            y.append(item)
            index += 1
        z.append(index)


makeAList(totalRequests, requests, requestIndex)
makeAList(totalNeighborhoods, neighborhoods, hoodIndex)


requestDict = dict(zip(requestIndex, requests))      #zipping these dictionaries allows for easy indexing/selection
hoodDict = dict(zip(hoodIndex, neighborhoods))


mostRequested = ""
requestedCount = 0
busyHood = ""
hoodCount = 0


for r in requests:                                              #returns the most common request, and the neighborhood with the most calls
    request_count = int(totalRequests.count(str(r)))
    if request_count > requestedCount:
        requestedCount = request_count
        mostRequested = r

for hood in neighborhoods:
    if len(hood) > 0:
        hood_count = int(totalNeighborhoods.count(str(hood)))
        if hood_count > hoodCount:
            hoodCount = hood_count
            busyHood = hood

print (str(mostRequested) + " seem to be our worse problem out there, Chief. Time to get on it.")     #I like using the time module when printing statements. It gives a more personable,
time.sleep(2)                                                                                           #interactive feel to the program. Sleep pauses the program long enough to give the illusion of typing
print ("We might want to focus on the " + str(busyHood) + " neighborhood, Boss. It looks like they need a lot of assistance there.")
time.sleep(2)
print ("Here, check this out: ")
time.sleep(2)

for h in hoodDict:
    print (h, hoodDict[h])

hoodNum = input("What was the number of the neighborhood you were looking for? ")    #select a neighborhood to return information on
hoodInt = int(hoodNum)

if hoodInt in hoodDict:
    bigHood = hoodDict[hoodInt]
    total = 0
    calls = []
    occurs = []
    climb = []
    sizes = []
    labels = []
    listOfLists = []


    with open("C:/Users/wwalk_000/desktop/311_data.csv") as file:
        pieReader = csv.DictReader(file)

        for p in pieReader:                                         #In building the pie charts initially, I found there were too many disparate requests for the visualization to be of
            if bigHood in p['NEIGHBORHOOD']:                        #any use. I had to make some adjustments
                type = p['REQUEST_TYPE']
                calls.append(type)
                total += 1
                if type not in climb:
                    climb.append(type)


        for c in climb:                                                 #I had some difficulty in trying to figure how to sort the list of comparative sizes, along with the appropriate neighborhood,
            blank = []                                                   #and only grab the largest 7 for the pie chart. This was the best I could do
            size = round(float(int(calls.count(c)) / int(total)), 3)
            blank.append(c)
            blank.append(size)
            listOfLists.append(blank)

        newList = sorted(listOfLists, key=lambda x: x[1])               #My solution was to bind the size values with the names, and then sort the lists by index
        labelLists = [newList[-7:len(newList)]]

        for l in labelLists:
            for i in l:
                labels.append(i[0])
                sizes.append(i[1])


        other = "Other"                                                     #To give perspective, I added an "Other" slice
        otherAmt = round(float((int(total) - sum(sizes)) / int(total)), 2)
        labels.append(other)
        sizes.append(otherAmt)

        patches, texts = plt.pie(sizes, shadow=True, startangle = 90)       #Builds the pie chart with corresponding data, legend, and title
        plt.legend(patches, labels, loc="best")
        plt.title(str(bigHood))
        plt.axis('equal')
        plt.tight_layout()
        plt.show()








