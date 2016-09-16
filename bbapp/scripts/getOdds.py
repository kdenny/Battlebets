import simplejson as json
import oauth2
import requests
import argparse
from pprint import pprint
import sys
import urllib
import urllib2
import oauth2
import os
import lxml
from datetime import datetime
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

from bbapp.models import *



def addOddsToGame(data,sport):
    today = datetime.now().strftime("%m/%d/%Y")

    if sport.lower() != 'nfl':

        for dm in data:
                ## Iterate through odds scraping results
                if 'home_short' in dm and 'away_short' in dm:
                    pkey = '{3}-{0}-{1}-{2}'.format(dm['home_short'], dm['away_short'], today, sport.lower())

                    q = Game.objects.filter(gamekey=pkey)

                    if len(q) == 0:
                        ## Build game object from odds scraping
                        game = Game()
                        game.league = sport
                        game.home_team = dm['home']
                        game.home_odds = dm['MATCH_ODDS']['home']
                        game.away_team = dm['away']
                        game.away_odds = dm['MATCH_ODDS']['away']
                        game.over_under = float(str(dm['Over/Under']).replace("+","").replace("-",""))
                        game.date = today
                        game.gamekey = pkey
                        game.save()

                    else:
                        ## Update game object with odds
                        for gamt in q:
                            gamt.home_team = dm['home']
                            gamt.home_odds = dm['MATCH_ODDS']['home']
                            gamt.over_under = float(str(dm['Over/Under']).replace("+","").replace("-",""))
                            gamt.away_team = dm['away']
                            gamt.away_odds = dm['MATCH_ODDS']['away']
                            gamt.save()

    else:

        decipherName = {
            'Green Bay Packers' : 'GB',
            'New York Jets' : 'NYJ',
            'Buffalo Bills' : 'BUF',
            'New Orleans Saints' : 'NO',
            'New York Giants' : 'NYG',
            'Dallas Cowboys' : 'DAL',
            'Washington Redskins' : 'WAS',
            'San Francisco 49ers' : 'SF',
            'Carolina Panthers' : 'CAR',
            'Cincinnati Bengals' : 'CIN',
            'Pittsburgh Steelers' : 'PIT',
            'Baltimore Ravens' : 'BAL',
            'Cleveland Browns' : 'CLE',
            'Tennessee Titans' : 'TEN',
            'Detroit Lions' : 'DET',
            'Kansas City Chiefs' : 'KC',
            'Houston Texans' : 'HOU',
            'Tampa Bay Buccaneers' : 'TB',
            'Arizona Cardinals' : 'AZ',
            'Atlanta Falcons' : 'ATL',
            'Oakland Raiders' : 'OAK',
            'Jacksonville Jaguars' : 'JAX',
            'San Diego Chargers' : 'SD',
            'Minnesota Vikings' : 'MIN',
            'Philadelphia Eagles' : 'PHL',
            'Chicago Bears' : 'CHI'
        }


        for dg in data:
            dg['home_short'] = decipherName[dg['home']]
            dg['away_short'] = decipherName[dg['away']]

            pprint(dg)

            if 'home_short' in dg and 'away_short' in dg:
                pkey = '{3}-{0}-{1}-{2}'.format(dg['home_short'], dg['away_short'], today, sport.lower())

                q = Game.objects.filter(gamekey=pkey)

                if len(q) == 0:
                        ## Build game object from odds scraping
                        game = Game()
                        game.league = sport
                        game.home_team = dg['home']
                        game.home_short = dg['home_short']
                        game.home_odds = dg['home_odds']
                        game.home_spread = dg['home_spread']
                        game.away_team = dg['away']
                        game.away_short = dg['away_short']
                        game.away_odds = dg['away_odds']
                        game.away_spread = dg['away_spread']
                        game.over_under = float(str(dg['over-under']))
                        game.date = dg['date']
                        game.gamekey = pkey
                        game.save()

                else:
                    ## Update game object with odds
                    for gamt in q:
                        gamt.league = sport
                        gamt.home_team = dg['home']
                        gamt.home_odds = dg['home_odds']
                        gamt.home_short = dg['home_short']
                        gamt.home_spread = dg['home_spread']
                        gamt.away_team = dg['away']
                        gamt.away_odds = dg['away_odds']
                        gamt.away_short = dg['away_short']
                        gamt.away_spread = dg['away_spread']
                        gamt.over_under = float(str(dg['over-under']))
                        gamt.save()




def getGames(sport):
    """Prepares OAuth authentication and sends the request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    # url_params = url_params or {}
    # url = 'https://{0}{1}{2}'.format(host, urllib.quote(path.encode('utf8')))

    events = {}
    url = 'http://odds.betgun.com/makeBB.php?id={0}'.format(sport)
    print(url)

    conn = urllib2.urlopen(url, None)
    try:
        soup = BeautifulSoup(conn, 'xml')
        games = []

        events = soup.find_all('event')
        # print memoryElem.get('unit') # attribute

        # tree = ET.parse(soup)
        # root = tree.getroot()


        for allsub in events:
            edict = dict()
            edict['away'] = allsub['awayteam']
            edict['home'] = allsub['hometeam']
            edict['datetime'] = str(allsub['datetime'])
            edict['date'] = str(allsub['date'])
            subevents = allsub.find_all('subevent')
            for sub in subevents:
                # pprint(sub)

                type = str(sub['dsymbol'])
                sel = sub.find_all('selection')

                if type == 'MATCH_ODDS':
                    sdict = dict()
                    for s in sel:
                        n = str(s['name'])
                        sdict[n] = str(s['odds'])
                        nt = float(sdict[n])
                        nto = int(nt * 100.0)
                        sdict[n] = '+' + str(nto)

                else:
                    if type == 'B_H':
                        type = 'Handicap'
                        for s in sel:
                            sdict = str(s['value'])
                    if type == 'B_SP':
                        type = 'Over/Under'
                        for s in sel:
                            sdict = str(s['value'])


                if type in ['Handicap', 'Over/Under', 'MATCH_ODDS']:
                    edict[type] = sdict

            games.append(edict)


        # for event in root.iter('event'):
        #     print(event.attrib)
        #     pprint(event)
        #     game = dict()
        #     soupd = event.find_all('awayteam')
        #     pprint(soupd)
        #     game['away'] = event.awayteam
        #     pprint(game)

    finally:
        conn.close()

    # url.add_header('Authorization', 'Basic U03MyOT23YbzMDc6d3c3O1DQ1')

    games = addShortNames(games)

    return games


def addShortNames(odds):

    newlist = []

    for oGame in odds:

        hote = oGame['home']
        awte = oGame['away']

        shortTeams = {
            'Minnesota' : 'MIN',
            'Yankees' : 'NYY',
            'Tampa Bay' : 'TB',
            'Baltimore' : 'BAL',
            'Toronto' : 'TOR',
            'Chicago White Sox' : 'CWS',
            'Cleveland' : 'CLE',
            'Detroit' : 'DET',
            'Washington' : 'WAS',
            'Milwaukee' : 'MIL',
            'San Diego' : 'SD',
            'Cincinnati' : 'CIN',
            'Arizona' : 'AZ',
            'Colorado' : 'COL',
            'Chicago Cubs' : 'CHC',
            'Miami' : 'MIA',
            'Houston' : 'HOU',
            'Kansas City' : 'KC',
            'Mets' : 'NYM',
            'Atlanta' : 'ATL',
            'Dodgers' : 'LAD',
            'Pittsburgh' : 'PIT',
            'Boston' : 'BOS',
            'Texas' : 'TEX',
            'Oakland' : 'OAK',
            'Angels' : 'LAA',
            'Philadelphia' : 'PHL',
            'San Francisco' : 'SFO',
            'St. Louis' : 'STL',
            'Seattle' : 'SEA'
            }

        for sn in shortTeams:
            if sn in hote:
                oGame['home_short'] = shortTeams[sn]
            elif sn in awte:
                oGame['away_short'] = shortTeams[sn]

        pprint(oGame)
        newlist.append(oGame)

    return newlist


def getNFLGames():
    """Prepares OAuth authentication and sends the request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    # url_params = url_params or {}
    # url = 'https://{0}{1}{2}'.format(host, urllib.quote(path.encode('utf8')))

    events = {}
    url = 'http://sportsfeeds.bovada.lv/basic/NFL.xml'
    print(url)

    conn = urllib2.urlopen(url, None)
    try:
        soup = BeautifulSoup(conn, 'xml')
        games = []

        dates = soup.find_all('Date')

        for da in dates:

            currentdate = str(da)[str(da).index('DTEXT="')+7:str(da).index('TS=')-2]

            events = da.find_all('Event')

            # pprint(events)

            # print memoryElem.get('unit') # attribute

            # tree = ET.parse(soup)
            # root = tree.getroot()


            for allsub in events:

                comp = allsub.find_all('Competitor')

                # pprint(comp)

                home_str = str(comp[0])
                away_str = str(comp[1])

                game = {}

                name_start = home_str.index('NAME') + 6
                name_end = home_str.index('NUM') - 2

                game['home']  = home_str[name_start:name_end]

                name_start = away_str.index('NAME') + 6
                name_end = away_str.index('NUM') - 2


                game['away'] = away_str[name_start:name_end]


                home_lines = home_str[home_str.index('Line'):]

                away_lines = away_str[away_str.index('Line'):]


                game['home_spread'] = home_lines[home_lines.index('NUMBER="')+8:home_lines.index('TS')-2]
                game['away_spread'] = away_lines[away_lines.index('NUMBER="')+8:away_lines.index('TS')-2]

                home_odds = home_lines[home_lines.index('Odds'):]


                away_odds = away_lines[away_lines.index('Odds'):]

                game['home_odds'] = home_odds[home_odds.index('Line="')+6:home_odds.index('MULTIPLIER')-2]
                game['away_odds'] = away_odds[away_odds.index('Line="')+6:away_odds.index('MULTIPLIER')-2]


                time_txt = str(allsub.find_all('Time'))
                over_under_txt = str(allsub.find_all('Line')[2])

                game['over-under'] = over_under_txt[over_under_txt.index('NUMBER="')+8:over_under_txt.index('TS="')-2].replace("\xc2\xbd",".5")

                game['time'] = time_txt[time_txt.index('TTEXT="')+7:time_txt.index('/>')-1]

                game['date'] = currentdate

                games.append(game)



    finally:
        conn.close()

    # url.add_header('Authorization', 'Basic U03MyOT23YbzMDc6d3c3O1DQ1')


    return games


def getnbagames():
    events = {}
    url = 'http://www.donbest.com/nba/odds/'
    print(url)

    conn = urllib2.urlopen(url, None)
    try:
        soup = BeautifulSoup(conn)
        # pprint(soup)

        holder = soup.find_all('div')
        for h in holder:
            print("")
            pprint(h)
            if 'class' in h:
                pprint(h['class'])

    finally:
        conn.close()

    # url.add_header('Authorization', 'Basic U03MyOT23YbzMDc6d3c3O1DQ1')




# def readGeojson(file):
#     import csv
#     file = 'http://www2.census.gov/geo/docs/maps-data/data/rel/2010_Census_Tract_to_2010_PUMA.txt'
#     response = urllib2.urlopen(file)
#     cr = csv.reader(response)
#     return a

