import csv
import pandas

file = open("C:/Users/wwalk_000/Desktop/jail.csv", newline='')
reader = csv.DictReader(file)

numBlack = 0
numWhite = 0
num28YearsOld = 0
targetDate = '2018-01-01'
valWhite = 'W'
valBlack = 'B'

for row in reader:
    if row['date'] == targetDate:
        if int(row['agecurr']) == 28:
            num28YearsOld = num28YearsOld + 1
        if row['race'] == valWhite:
            numWhite = numWhite + 1
        elif row['race'] == valBlack:
            numBlack = numBlack + 1

file.close()

print("Total black population: " + str(numBlack))
print ("Total White population: " + str(numWhite))
print ("Total 28-year-old population: " + str(num28YearsOld))

percentBlack = float(numBlack / (numBlack + numWhite))

print ("percent Black inmates: " + str(percentBlack))