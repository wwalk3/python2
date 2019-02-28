# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 15:22:20 2018
@author: puter
"""
cryptos = {
    'platforms':
        {
            'description': 'can make stuff out these',
            'eth': {'name': 'Ethereum', 'year': 2014, 'priceUSD': 193},
            'ada': {'name': 'Cardano', 'year': 2016, 'priceUSD': .06},
            'eos': {'name': 'EOS', 'year': 2017, 'priceUSD': 4.85},
            'neo': {'name': 'NEO', 'year': 2014, 'priceUSD': 17.49}

        },

    'computing, data management, and cloud services':
        {
            'description': 'paradigm shifters',
            'gnt': {'name': 'Golem', 'year': 2016, 'priceUSD': .12},
            'sia': {'name': 'Siacoin', 'year': 2015, 'priceUSD': .01},
            'storj': {'name': 'Storj', 'year': 2015, 'priceUSD': .23},
            'hot': {'name': 'Holotoken', 'year': 2017, 'priceUSD': .001}
        },

    'payments':
        {'description': 'you can pay for stuff with these',
         'ltc': {'name': 'Litecoin', 'year': 2011, 'priceUSD': 51.00},
         'etn': {'name': 'Electroneum', 'year': 2016, 'priceUSD': .0051},
         'nano': {'name': 'NANO', 'year': 2014, 'priceUSD': 2.05},
         'doge': {'name': 'Dogecoin', 'year': 2013, 'priceUSD': .01}
         }

}

for x in cryptos:
    print (x)

entry = input("Choose an option from above: ")

if entry in cryptos:
    for i in cryptos[entry].keys():
        print (i)

deeper = input("Which would you like to know more about? ")

if deeper in cryptos[entry]:
    for d in cryptos[entry][deeper]:
        print (d, '\t', cryptos[entry][deeper][d])

# search = input("Anything else you would like to know about? ")





