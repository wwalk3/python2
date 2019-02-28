import csv

file = open("C:/Users/wwalk_000/Desktop/311_data.csv")
readit = csv.DictReader(file)

count = 0

for row in readit:
    if "Lawrenceville" in row['NEIGHBORHOOD']:
        count += 1

print ("The data shows that {0} calls were made from Lawrenceville".format(count))