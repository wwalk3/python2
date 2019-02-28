import csv

dataFile = open("C:/Users/wwalk_000/desktop/311_data.csv")
reader = csv.DictReader(dataFile)

# def dict(requests()):
#     return {"Request Type":None, "Count":None}
#
# data = {requests}

requests = []
data = {}

def requests


for row in reader:
    if row['REQUEST_TYPE'] not in requests:
        requests.append(row['REQUEST_TYPE'])
        count = 1
        requests[row].values().append(count)
    elif row['REQUEST_TYPE'] in requests.keys():
        count += 1
        requests[row].values().update(count)

for i in data.keys():
    print (i[0], '/t', i[1])




#
# dict = {"data":"count"}
# requests = []
#
# for row in reader:
#     if row['REQUEST_TYPE'] not in requests:
#         requests.append(row['REQUEST_TYPE'])
#         count = 1
#         requests[row][1].append(count)
#     if row['REQUEST_TYPE'] in requests:
#         count += 1
#         requests[row][1].append(count)

# for x in requests:
#     print (x(0), '/t', x(1))


# number = 0
# numCount = str(number)
# name = str("count" + '_' + numCount)
#
# for x in requests:
#     for row in reader:
#         if x in row['REQUEST_TYPE']:
#             name += 1
#             x.append(name)
#
#         number += 1
#
# for item in requests:
#     print (item)

# for x in requests():
#     requests.append(reader.count(x))
#     print (x(0), '\t', x(1))



# for x in requestData:
#     if x in row['REQUEST_TYPE']:
#         count = 0
#         count += 1
#         requestData[x].values(count)
#
# for i in requestData:
#     print (i, '\t', requestData[i])