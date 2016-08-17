import urllib2
import json
from pprint import pprint
import lxml
from bs4 import BeautifulSoup


import os
import sys
# path = '/home/kdenny37/Battlebets/'
# if path not in sys.path:
#     sys.path.append(path)
#
# os.chdir(path)
#
# os.environ['DJANGO_SETTINGS_MODULE'] = 'Battlebets.settings'
#
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()

from bbapp.models import *
from datetime import datetime, timedelta



def fixScores(currentScores, sport):

    longNames = ['San', 'St.', 'NY', 'LA', 'Tampa', 'Chicago', 'Kansas']

    currentTime = datetime.now()
    currentHour = currentTime.hour
    currentDay = currentTime.day


    print("")
    print("Current hour is {0}".format(currentHour))

    today = currentTime.strftime("%m/%d/%Y")

    if currentHour < 12:
        yesterday = datetime.now() - timedelta(days=1)
        print("Showing yesterday's games")
        today = yesterday.strftime("%m/%d/%Y")

    elif currentHour >= 19:
        print ("It's game time!")

    for cs in currentScores:
        pprint(cs)
        pkey = '{0}-{1}-{2}'.format(cs['Home_Short'], cs['Away_Short'], today)

        q = Game.objects.filter(gamekey=pkey)

        if len(q) == 0:
            ## Build game object
            game = Game()
            game.league = sport
            game.home_short = cs['Home_Short']
            game.away_short = cs['Away_Short']
            game.status = cs['Status']
            if cs['Status'] == 'Upcoming':
                game.game_time = cs['Game Time']
            game.date = today
            game.gamekey = pkey
            game.save()

        else:
            ## Update game objects
            for gamt in q:
                if gamt.status != 'Historic' and gamt.status != 'Final':
                    gamt.home_short = cs['Home_Short']
                    gamt.away_short = cs['Away_Short']
                    gamt.status = cs['Status']
                    if gamt.status != 'Upcoming':
                        gamt.home_score = cs['Home_Score']
                        gamt.away_score = cs['Away_Score']
                    if cs['Status'] == 'Upcoming':
                        gamt.game_time = cs['Game Time']
                    gamt.save()

                if cs['Status'] == 'Final':
                    ## Process games that have ended
                    gamt.home_score = cs['Home_Score']
                    gamt.away_score = cs['Away_Score']
                    gamt.status = 'Historic'
                    gamt.save()
                    winp = cs['Winner']
                    gametx = gamt.gamekey
                    gameitems = gametx.split("-")
                    if winp == 'Home':
                        winner = gameitems[0]
                    elif winp == 'Away':
                        winner = gameitems[1]

                    gamebets = Bet.objects.filter(game=pkey)

                    for gbet in gamebets:
                        new = 0
                        ## Update all bets with the winner of bet
                        if gbet.bet_status == 'Accepted':
                            totalscore = float(gbet.game.home_score) + float(gbet.game.away_score)
                            overunder = float(gbet.game.over_under)
                            if gbet.bet_type == 'even':
                                new = 1
                                if gbet.bet_selection == gbet.game.home_team:
                                    if winp == 'Home':
                                        gbet.bet_status = 'user1win'
                                        print("User 1 won bet")
                                    else:
                                        gbet.bet_status = 'user2win'
                                        print("User 2 won bet")
                                elif gbet.bet_selection == gbet.game.away_team:
                                    if winp == 'Home':
                                        gbet.bet_status = 'user2win'
                                    else:
                                        gbet.bet_status = 'user1win'
                            elif gbet.bet_type == 'over':
                                new = 1
                                if totalscore > overunder:
                                    gbet.bet_status = 'user1win'
                                else:
                                    gbet.bet_status = 'user2win'
                            elif gbet.bet_type == 'under':
                                new = 1
                                if totalscore < overunder:
                                    gbet.bet_status = 'user1win'
                                else:
                                    gbet.bet_status = 'user2win'



                        gbet.changed_date = datetime.now()
                        gbet.save()

                        user1 = gbet.user1
                        user2 = gbet.user2


                        ## Notify users of status of bet
                        if not user1.notifications.exists():
                            bet_notice = user1.notifications.create(bet=gbet,
                                                                   sender=user2)
                        if not user2.notifications.exists():
                            bet_notice2 = user2.notifications.create(bet=gbet,
                                                                   sender=user1)

                        if new == 1:

                            bet_notice = Notification()
                            bet_notice.bet = gbet
                            bet_notice.user = gbet.user1
                            bet_notice.sender = gbet.user2
                            bet_notice.save()

                            user1.notifications.add(bet_notice)

                            bet_notice2 = Notification()
                            bet_notice2.bet = gbet
                            bet_notice2.user = gbet.user2
                            bet_notice2.sender = gbet.user1
                            bet_notice2.save()

                            user2.notifications.add(bet_notice2)



def request():
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
    sport = 'baseball'
    league = 'MLB'
    url = 'http://espn.go.com/mlb/bottomline/scores'.format(league)


    # print u'Querying {0} ...'.format(url)

    conn = urllib2.urlopen(url, None)

    try:
        soup = BeautifulSoup(conn, 'html.parser')
        games = []
        print()
 #       pprint(soup)

    finally:
        conn.close()


    return soup


def chefThatSoup(soup):


    longNames = ['San', 'St.', 'NY', 'LA', 'Tampa', 'Chicago', 'Kansas']

    gameScores = []

    resultsText = str(soup)

    gamesList = resultsText.split("s_left")

    gameI = resultsText.index("s_left")
    #pprint(gamesList)

    for game in gamesList:
        gameR = {}

        gameN = game.split('%20')

        extracount = 0

        # print(gameN)
        # print("")

        if gameN[0].split('=')[1] != '120&amp;mlb;_s_stamp':


            ## Process Away team

            if gameN[0].split('=')[1].replace("^","") not in longNames:
                gameR['Away_Team'] = gameN[0].split('=')[1]
            else:
                gameR['Away_Team'] = gameN[0].split('=')[1] + ' ' + gameN[1]
                extracount += 1

            ## Process Away team score

            hsloc = 1 + extracount

            flagcheck = 2 + extracount

            if gameN[flagcheck] != '':
                gameR['Away_Score'] = 'TBD'
                gameR['Status'] = 'Upcoming'
            else:
                gameR['Away_Score'] = gameN[hsloc]
                gameR['Status'] = 'In Progress'


            ## Process Home team name and score

            if gameR['Status'] == 'In Progress':
                atloc = 4 + extracount

                if gameN[atloc].replace('^','') not in longNames:
                    gameR['Home_Team'] = gameN[atloc]
                    gameR['Home_Score'] = gameN[(atloc+1)]
                    if len(gameN) > (atloc+3):
                        if len(gameN[(atloc+3)].split(")")) > 0:
                            gameR['Inning'] = gameN[(atloc+2)].replace("(","") + ' ' + gameN[(atloc+3)].split(")")[0]

                else:
                    gameR['Home_Team'] = gameN[atloc] + ' ' + gameN[(atloc+1)]
                    gameR['Home_Score'] = gameN[(atloc+2)]
                    if len(gameN) > (atloc+4):
                        if len(gameN[(atloc+4)].split(")")) > 0:
                            gameR['Inning'] = gameN[(atloc+3)].replace("(","") + ' ' + gameN[(atloc+4)].split(")")[0]


                if 'Inning' not in gameR:
                    gameR['Inning'] = ''



            ## Process home team name and game time


            else:
                atloc = 2 + extracount

                if str(gameN[atloc]).replace("^","") not in longNames:
                    gameR['Home_Team'] = gameN[atloc]
                    gameR['Game Time'] = gameN[(atloc+1)].replace("(","") + ' ' + gameN[(atloc+2)] + ' ' + gameN[(atloc+3)].split(")")[0]

                else:
                    gameR['Home_Team'] = gameN[atloc] + ' ' + gameN[(atloc+1)]
                    gameR['Game Time'] = gameN[(atloc+2)].replace("(","") + ' ' + gameN[(atloc+3)] + ' ' + gameN[(atloc+4)].split(")")[0]



            if '^' in gameR['Home_Team']:
                gameR['Status'] = 'Final'
                gameR['Winner'] = 'Home'

            elif '^' in gameR['Away_Team']:
                gameR['Status'] = 'Final'
                gameR['Winner'] = 'Away'

            if gameR['Status'] == 'Final':
                gameR['Inning'] = 'Final'



            gameScores.append(gameR)

    return gameScores


def processScores(scores):

    shortTeams = {
        'Minnesota' : 'MIN',
        'NY Yankees' : 'NYY',
        'Tampa Bay' : 'TB',
        'Baltimore' : 'BAL',
        'Toronto' : 'TOR',
        'Chicago Sox' : 'CWS',
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
        'NY Mets' : 'NYM',
        'Atlanta' : 'ATL',
        'LA Dodgers' : 'LAD',
        'Pittsburgh' : 'PIT',
        'Boston' : 'BOS',
        'Texas' : 'TEX',
        'Oakland' : 'OAK',
        'LA Angels' : 'LAA',
        'Philadelphia' : 'PHL',
        'San Francisco' : 'SFO',
        'St. Louis' : 'STL',
        'Seattle' : 'SEA'
        }

    for sc in scores:
        sc['Away_Short'] = shortTeams[sc['Away_Team'].replace('^','')]
        sc['Home_Short'] = shortTeams[sc['Home_Team'].replace('^','')]


    return scores





def doScoresScrape():

    re = request()

    scoresD = chefThatSoup(re)

    scores = processScores(scoresD)

    return scores




