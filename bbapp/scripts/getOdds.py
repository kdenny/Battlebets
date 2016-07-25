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

    for dm in data:
            ## Iterate through odds scraping results
            if 'home_short' in dm and 'away_short' in dm:
                pkey = '{0}-{1}-{2}'.format(dm['home_short'], dm['away_short'], today)

                q = Game.objects.filter(gamekey=pkey)

                if len(q) == 0:
                    ## Build game object from odds scraping
                    game = Game()
                    game.league = sport
                    game.home_team = dm['home']
                    game.home_odds = dm['MATCH_ODDS']['home']
                    game.away_team = dm['away']
                    game.away_odds = dm['MATCH_ODDS']['away']
                    game.date = today
                    game.gamekey = pkey
                    game.save()

                else:
                    ## Update game object with odds
                    for gamt in q:
                        gamt.home_team = dm['home']
                        gamt.home_odds = dm['MATCH_ODDS']['home']
                        gamt.away_team = dm['away']
                        gamt.away_odds = dm['MATCH_ODDS']['away']
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
            pprint(allsub)
            edict = dict()
            pprint("")
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

            # pprint(edict)
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

