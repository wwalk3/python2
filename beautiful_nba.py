from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 50)
pd.set_option('display.width', 1000)

url = "https://www.basketball-reference.com/leagues/NBA_2019_per_game.html"
nba_main = requests.get(url)
nbaSoup = BeautifulSoup(nba_main.text, 'html.parser')


name = nbaSoup.findAll('td', attrs = {"data-stat":"player"})
attributes = nbaSoup.findAll(attrs = {"data-stat"})
table = nbaSoup.findAll('tr', class_= "full_table")

names = []
points = []
effective = []
attempts = []
assists = []
steals = []
blocks = []
rebounds = []


for i in table:
    player = i.find(attrs = {"data-stat" : "player"})
    efg = i.find(attrs = {"data-stat" : "efg_pct"})
    ppg = i.find(attrs = {"data-stat" : "pts_per_g"})
    stl = i.find(attrs = {"data-stat" : "stl_per_g"})
    blk = i.find(attrs = {"data-stat" : "blk_per_g"})
    fga = i.find(attrs = {"data-stat" : "fga_per_g"})
    ast = i.find(attrs = {"data-stat" : "ast_per_g"})
    reb = i.find(attrs = {"data-stat" : "trb_per_g"})
    names.append(player.text)
    points.append(ppg.text)
    effective.append(efg.text)
    attempts.append(fga.text)
    assists.append(ast.text)
    steals.append(stl.text)
    blocks.append(blk.text)
    rebounds.append(reb.text)

stats = pd.DataFrame({'Player' : names,
                        'Points Per Game' : points,
                        'eFG%' : effective,
                        'Attempts' : attempts,
                        'Assists' : assists,
                        'Steals' : steals,
                        'Blocks' : blocks,
                        'Rebounds' : rebounds})

print (stats)


# <td class="right " data-stat="stl_per_g">0.8</td> steals
# <td class="right " data-stat="blk_per_g">0.4</td> blocks
# <td class="right " data-stat="fga_per_g">19.4</td> Field Goal Attempts
# <td class="right " data-stat="efg_pct">.604</td> eFG%
# <td class="right " data-stat="ast_per_g">1.7</td> Assists
# <td class="right " data-stat="trb_per_g">2.9</td> total rebounds


# print (nbaSoup.contents)



# <td class="right " data-stat="fg_per_g">8.4</td> FG%
# <td class="right non_qual" data-stat="pts_per_g">9.8</td> Points Per Game
#<td class="left " data-append-csv="adebaba01" data-stat="player" csk="Adebayo,Bam"><a href="/players/a/adebaba01.html">Bam Adebayo</a></td>