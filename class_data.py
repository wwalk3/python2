import csv

# peerinfo = {'name':[],'hobbies':[],
#             'siblings':(),
#             'hometown':(),
#             'age':[],
#             'cities':[],
#             'languages': {'language':[], 'proficiency': []}
#             }

peerinfo = {'name':["Hi! What is your name? ", []],'hobbies':[],
            'siblings':(),
            'hometown':(),
            'age':[],
            'cities':[],
            'languages': {'language':[], 'proficiency': []}
            }

name = input("Hi! What is your name? ")
peerinfo['name'] = name

age = input("Nice to meet you {0}! How old are you?".format(name))
peerinfo['age'] = age

sibling = input("How many siblings do you have, {0}? ".format(name))
peerinfo['siblings'] = sibling

hometown = input("Cool! What city are you from? ")
peerinfo['hometown'] = hometown

cities = []
other_cities = input("Have you lived anywhere else? yes/no? ")

if other_cities == "yes":
    many = input("Yeah?! How many other places?! ")
    count = int(many)

    for x in range(count):
        x += 1
        ask = input("What is city number {0}? ".format(x))
        cities.append(ask)
        x +=1

peerinfo['cities'] = cities
hobbies = []

for i in range(1, 4):
    entry = input("What is your #{0} hobby? ".format(i))
    hobbies.append(entry)

peerinfo['hobbies'] = hobbies
# print (peerinfo)




