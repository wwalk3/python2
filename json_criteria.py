import csv
import json

capJSON = "C:/Users/wwalk_000/Desktop/work_folder/capital_json.json"

with open("C:/Users/wwalk_000/Desktop/work_folder/capital_projects_data.csv") as dataFile:
    reader = csv.DictReader(dataFile)
    headers = reader.fieldnames
    dict = {}
    query_dict = {"fiscal_year": [headers[8]],
                    "start_date": [headers[9]],
                    "area": [headers[3]],
                    "asset_type": [headers[7]],
                    "planning_status": [headers[5]]
                  }
    for row in reader:
        id = row["id"]
        dict[id] = row

    for keys in query_dict:
        print (keys)

    query = input("What would you like to know more about? ")

    for line in headers:
        if query in query_dict:
                # qKey = query
                # findIt = query_dict.values(qKey)
                # print (findIt.items)
                data = {}
                if query == "fiscal year":
                    for y in headers[8]:
                        if y not in data:
                            data.update(y)
                            print (data.keys())
                elif query == "start_date":
                    for s in headers[9]:
                        if s not in data:
                            data.update(s)
                            print (data.keys())
                elif query == "area":
                    for p in headers[3]:
                        if p not in data:
                            data.update(p)
                            print (data.keys(p))
                elif query == "asset type":
                    for t in headers[7]:
                        if t not in data:
                            data.update(t)
                            print (data.keys(t))
                elif query == "planning status":
                    for s in headers[5]:
                        if s not in data:
                            data.update(s)
                            print (data.keys(s))


with open(capJSON, "w") as jsonFile:
    jsonFile.write(json.dumps(keep, indent = 4))

