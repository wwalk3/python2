import json
from bs4 import BeautifulSoup as bs
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

osAPIKEY = "75e6b4a0a0c476064edadcd550eb1911"
ppKEY = {'X-API-Key': "FJEmyb29STmcvfi5w3qYMYx7U1ufS0J3dUJhSu2h"}


# This program has 3 main functions:
# 1. to give a list of a state's legislators and their biggest donors.
# 2. To allow further investigation into a chosen legislator and their top big money donors
# 3. To be able to search for organizations that give to candidates, and the bills they lobby
# 4. To search through bills lobbied by the organization, and investigate legislators on the committees who are also in part funded by the organization.

# In the future, I would like to turn this program into a fully interactive app, with user-friendly GUI
# I would like to be able to return custom reports, give more information on selected bills, and be able to perform more
# useful analysis operations. I would also like to return more individual legislator information in order to directly connect the user with a desired legislator's contact information.

# THREE DISCLAIMERS:
# 1. This program is currently linear. It will walk you through steps and then complete. This will be remedied in future programming.
# 2. The initial report runs through multiple url calls to gather data on numerous individuals. Depending on the size of the state (its number of legislators), the initial step can take several minutes.
# 3. A small minority of states (i.e., Georgia) have different data-keeping structures that will cause the program to return an error. This will be addressed in further programming.

# Have fun and MAKE SURE YOUR REPRESENTATIVES HEAR YOU!


state = input("What state would you like to search for? Please enter two-letter abbreviation: ")
print ("Thanks! Please hold while I retrieve your info!")

idURL = "http://www.opensecrets.org/api/?method=getLegislators&id=" + str(state) + "&apikey=" + str(osAPIKEY) + "&output=json"
idReq = requests.get(idURL)
errors = 0
nameList = []
idList = []
candidates = 0
runningTotal = 0
avg = 0
male = 0
female = 0
totalTenure = 0
moneySpent = 0
candIndex = 0
candIndexList = []
names = []
COH = []
biggestCON = []
biggestContribution = []
percentage = []
bigMoney = []


if int(idReq.status_code) == 200:                              #checks to make sure request goes through
    idJSON = json.loads(idReq.text)
    idLevel = idJSON['response']['legislator']

    for i in idLevel:                                          #this is the individual candidate in the list of state legislators
        att = i['@attributes']
        idNo = att['cid']
        name = att['firstlast']
        candIndex += 1                                         #builds a list to index for user-friendly usage, will index in the dataframe
        candIndexList.append(candIndex)
        nameList.append(name)
        idList.append(idNo)
        if att['gender'] == 'M':                               # while here, the program does some scraping for later usage, such as male/female ratio, and builds dictionary linking candidates to their ID numbers
            male += 1
        elif att['gender'] == 'F':
            female += 1

    candList = dict(zip(nameList, idList))
    candIDList = dict(zip(candIndexList, idList))

    for n in candList:                                          #this iterates through a dictionary of candidates, rather than making individual calls for each candidate in the previous API
        cid = candList[n]
        getSummary = "http://www.opensecrets.org/api/?method=candSummary&cid=" + str(cid) + "&cycle=2018&apikey=" + str(osAPIKEY) + "&output=json"
        sumGet = requests.get(getSummary)

        if int(sumGet.status_code) == 200:                       # checks for any errors in recreating the url
            sumDict = json.loads(sumGet.text)
            sum = sumDict['response']['summary']['@attributes']
            candidates += 1
            tenure = 2019 - int(sum['first_elected'])
            totalTenure = totalTenure + tenure
            moneySpent = moneySpent + float(sum['spent'])
            runningTotal = runningTotal + float(sum['cash_on_hand'])  #all of this builds stats for total legislature report

        else:
            errors += 1

        getContributor = "https://www.opensecrets.org/api/?method=candContrib&cid=" + str(cid) + "&cycle=2018&apikey=" + str(osAPIKEY) + "&output=json"
        conGet = requests.get(getContributor)

        if int(conGet.status_code) == 200:
            conJSON = json.loads(conGet.text)
            conLevel = conJSON['response']['contributors']['contributor']
            con = ""
            conAmount = 0
            money = 0
            for row in conLevel:
                conName = row['@attributes']['org_name']
                conMoney = row['@attributes']['total']
                if int(conMoney) > conAmount:
                    conAmount = int(conMoney)
                    con = conName
                money = money + int(conMoney)

            percent = (round((float(conAmount)) / float(sum['total']), 3)) * 100
            BigMoney = (round(float(money) / float(sum['total']), 3)) * 100
            names.append(sum['cand_name'])
            COH.append(sum['cash_on_hand'])
            biggestCON.append(con)
            biggestContribution.append(conAmount)
            percentage.append(percent)
            bigMoney.append(BigMoney)

        else:
            errors += 1

    data = pd.DataFrame({'Candidate': names,
                         'Cash On Hand': COH,
                         'Biggest Donor': biggestCON,
                         'Donor Amount': biggestContribution,
                         '% of Total Funds': percentage,
                         '% Big Money': bigMoney}, index=candIndexList)

    print(data)

    print("\n" * 2)

    avg = int(runningTotal / candidates)
    print("*" * 25)
    print("$" + str(avg) + " on hand per candidate")
    print("*" * 25)
    if female > 0:
        ratio = int(male / female)
        print("The ratio of male to female candidates is " + str(ratio) + ":1")
    else:
        print("There are no women federal representatives from this state")
    print("*" * 25)
    avgTenure = int(totalTenure / candidates)
    print("The average tenure is " + str(avgTenure) + " years")
    print("*" * 25)
    moneyINT = int(moneySpent)
    print("A total of $" + str(moneyINT) + " has been spent by winning campaigns in " + str(state).upper() + " during the 2018 cycle.")
    print("*" * 25)
    if errors < 1 or errors > 1:
        print("with " + str(errors) + " errors")
    else:
        print("With " + str(errors) + " error")

else:
    errors += 1

print ('\n' * 2)


candSearch = input("Enter the number of the candidate would you like to look up: ")
searchNo = int(candSearch)

if searchNo in candIDList:
    candID = candIDList[searchNo]

############################################################    Integrate into previous contributor code
getContributor = "https://www.opensecrets.org/api/?method=candContrib&cid=" + str(candID) + "&cycle=2018&apikey=" + str(osAPIKEY) + "&output=json"
conGet = requests.get(getContributor)
conList = []
conTotal = []
indexList = []

if int(conGet.status_code) == 200:
    conJSON = json.loads(conGet.text)
    conLevel = conJSON['response']['contributors']['contributor']
    indexNum = 0

    for i in conLevel:
        conName = i['@attributes']['org_name']
        conMoney = i['@attributes']['total']
        conList.append(conName)
        conTotal.append(conMoney)
        indexNum += 1
        indexList.append(indexNum)


conDict = dict(zip(conList, conTotal))
indexDict = dict(zip(conList, indexList))
expIndex = 0
expMoney = 0
goRound = 0

for u in conDict:
    goRound += 1
    if int(conDict[u]) > expMoney:              #this chooses the highest contributor for "explosion" visual
        goRound = int(goRound)
        expMoney = int(conDict[u])
        expIndex = int(indexList[goRound]) - 1
##########################################################
sizes = conTotal
exp = [int(0) for e in range(len(conList))]
expReplace = int(int(expIndex) -1)
exp[expReplace] = exp[expReplace] + 0.2


plt.pie(sizes, explode=exp, labels=conList, shadow=True, autopct='%1.1f%%', startangle=140)
plt.title("Big Money Donors")
plt.axis('equal')
plt.show()


orgQuery = input("What organization would you like to know more about? \nSearch using one word from the organization: ") #begins search for organizations
orgRes = orgQuery.replace(' ', '')

orgURL = "https://www.opensecrets.org/api/?method=getOrgs&org=" + str(orgRes) + "&apikey=" + str(osAPIKEY) + "&output=json"
orgReq = requests.get(orgURL)
orgList = []
orgIdList = []

if int(orgReq.status_code) == 200:
    orgJSON = json.loads(orgReq.text)
    org = orgJSON['response']['organization']
    dictNum = 0
    numHead = []

    if type(org) is list:                         #checks for multiple entries
        for o in org:
            dictNum += 1
            orgName = o['@attributes']['orgname']
            orgId = o['@attributes']['orgid']

            orgList.append(orgName)
            orgIdList.append(orgId)
            numHead.append(dictNum)

    else:                                          #if only one entry
        orgName = org['@attributes']['orgname']
        orgId = org['@attributes']['orgid']
        dictNum = 1
        orgList.append(orgName)
        orgIdList.append(orgId)
        numHead.append(dictNum)

    firstDict = dict(zip(orgList, orgIdList))
    mainDict = dict(zip(numHead, orgIdList))
    displayDict = dict(zip(numHead, orgList))

    for i in displayDict:
        print (i, displayDict[i])

    print ('\n')
    searchIn = input("Please enter the number of the organization you're looking for: ")
    intSearch = int(searchIn)

    if intSearch in mainDict:
        search = mainDict[intSearch]
        orgNameForLater = str(displayDict[intSearch])

        searchURL = ("http://www.opensecrets.org/api/?method=orgSummary&id=" + str(search) + "&apikey=" + str(osAPIKEY) + "&output=json")
        searchReq = requests.get(searchURL)

        lobbyURL = ("https://www.opensecrets.org//orgs//lobby.php?id=" + str(search))
        lobbyGet = requests.get(lobbyURL)
        lobbySoup = bs(lobbyGet.text, 'html.parser')
        lobbyTable = lobbySoup.findAll('table')

        nameList = []
        billList = []
        realBillList = []

        if int(searchReq.status_code) == 200:
            searchJSON =json.loads(searchReq.text)
            searchLevel = searchJSON['response']['organization']['@attributes']
            print ('\n')
            print ('*' * 20)
            print ("Name: " + str(searchLevel['orgname']))
            print ("Total Contributions: $" + str(searchLevel['total']))
            print ("Money to Republicans: $" + str(searchLevel['repubs']))
            print ("Money to Democrats: $" + str(searchLevel['dems']))
            print ('Lobbying Dollars Spent: $' + str(searchLevel['lobbying']))
            print ("Soft Money: $" + str(searchLevel['soft']))


        for i in lobbyTable:
            lobbyName = i.findAll('tr')
            for l in lobbyName:
                lobby = l.findAll('td')
                o = [lobby[i] for i in range(0, len(lobby), 2)]
                billNo = [o[z] for z in range(0, len(o), 2)]
                billName = [o[y] for y in range(1, len(o), 2)]
                for n in billNo:
                    billList.append(n.text.rstrip("\n"))
                for b in billName:
                    nameList.append(b.text)

        for e in billList:
            f = e[1:len(e)]
            realBillList.append(f)

        billData = pd.DataFrame({"Bill Number": realBillList,
                                    "Bill Title": nameList})

        if int(len(realBillList)) > 0:
            print('Bills Lobbied:')
            print(billData)
        else:
            print('*' * 20)

        url = "https://www.opensecrets.org//orgs//recips.php?id=" + str(search)+ "&cycle=2018&state=&party=&chamber=&sort=A&page=1"  # needs to have id removed for customization
        req = requests.get(url)
        recip = bs(req.text, 'html.parser')
        page = recip.findAll('div', id="tab")

        recipList = []  # contains names of all recipients of contributions from the organization
        donNoList = []  # contains the corresponding amounts of contributions

        for i in page:
            pageNo = i.findAll('a')
            for o in pageNo:
                pages = o.text
                grabURL = ("https://www.opensecrets.org//orgs//recips.php?id=" + str(search) + "&cycle=2018&state=&party=&chamber=&sort=A&page=" + str(pages))
                grabGet = requests.get(grabURL)
                grabBS = bs(grabGet.text, 'html.parser')
                name = grabBS.findAll('tbody')

                for x in name:
                    cand = x.findAll('td', nowrap="")
                    money = x.findAll('td', class_="number")
                    moneyList = [m.text for m in money]
                    candList = [cand[c] for c in range(0, len(cand), 3)]

                    for t in moneyList:
                        donNoList.append(t)

                    for w in candList:
                        actual = w.text[0:-7]
                        recipList.append(actual)

        recipData = dict(zip(recipList, donNoList))
        compareList = []

        for r in recipData:
            cutItUp = r.split(", ")
            if len(cutItUp) >= 2:
                lastN = cutItUp[0]
                firstN = cutItUp[1]
                recipName = (str(firstN) + " " + str(lastN))
            else:
                recipName = cutItUp[0]
            compareList.append(recipName)

        compareMoneyDict = dict(zip(compareList, donNoList))

        billAsk = input("Enter a bill's official number to find out more about it: ")
        new = billAsk.replace('.','')
        newURL = ("https://api.propublica.org/congress/v1/115/bills/" + str(new) + ".json")
        newGet = requests.get(newURL, headers= ppKEY)
        newJSON = json.loads(newGet.text)
        billStuff = newJSON['results'][0]['title']
        committee = newJSON['results'][0]['committee_codes']
        committeeList = [c for c in committee]
        chamber = ""
        billMemList = []

        for com in committeeList:                                   #This builds a url based on whether the bill is from the House, the Senate, or a Joint committee
            if str(com[0]) is "S":
                chamber = "senate"
            if str(com[0]) is "H":
                if str(com[1]) is "J":
                    chamber = "joint"
                else:
                    chamber = "house"

            comMemURL = ("https://api.propublica.org/congress/v1/115/" + str(chamber) + "/committees/" + str(com) + ".json")
            comMemGet = requests.get(comMemURL, headers = ppKEY)
            comMemJSON = json.loads(comMemGet.text)
            comResults = comMemJSON['results']
            chair = comResults[0]['chair']
            members = comResults[0]['current_members']
            comName = comResults[0]['name']

            print ("\n")
            # print (comName)
            # print ("Chair: " + str(chair))
            # print ("*" * 30)
            # print ("Members:")
            for m in members:
                n = m['name']
                p = m['party']
                s = m['state']
                billMemList.append(n)
                #print (str(n) + " (" + str(p) + "-" + str(s) + ")")


        print ("These people received money from " + str(orgNameForLater) + " AND work on this bill: ")
        for compareName in compareMoneyDict:
            if compareName in billMemList:
                print (compareName, compareMoneyDict[compareName])


print ("\n")
print ("This work could not have been done without the published work of:")
print ("OpenSecrets.org and the Center for Responsive Politics")
print ("ProPublica.org and the ProPublica Data Store")
print ("\n")

print ("Please, try me again! And MAKE SURE YOUR REPRESENTATIVES HEAR YOU!")

