# Django
# import time
from datetime import *
from django.views.generic import UpdateView, ListView
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth import logout
from django.template import RequestContext, loader
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


# Python
import simplejson as json
import requests
from pprint import pprint

from bbapp.models import *



def makeBet(betselect, opponent, betamount, bettype, user1):

    madebet = False
    # print("You selected a bet on {0} with {1} for {2}".format(betselect, opponent, betamount))

    today = datetime.now().strftime("%m/%d/%Y")

    ishome = Game.objects.filter(home_team=betselect,date=today)
    isaway = Game.objects.filter(away_team=betselect,date=today)

    opponent_name = User.objects.filter(username=opponent)
    # print("Length of opponent name is {0}".format(len(opponent_name)))
    gamestr = ''

    if len(ishome) == 1:
        for r in ishome:
            if madebet == False:
                gamestr = r
                bet_selection = r.home_team
                # bet_odds = str(r.home_odds)
                # bet_odds = float(bet_odds.strip().replace('+',''))

    else:
        for r in isaway:
            if madebet == False and r.date == today:
                gamestr = r
                bet_selection = r.away_team
                # bet_odds = r.away_odds
                # bet_odds = float(bet_odds.strip().replace('+',''))


    for on in opponent_name:
        user2 = on

    bet_check = Bet.objects.filter(game=gamestr,user1=user1,user2=user2)

    if len(bet_check) == 0:

        if not gamestr.bet_set.exists():

            bet = gamestr.bet_set.create(user1=user1,
                                         bet_selection=bet_selection,
                                         user2=user2,
                                         bet_value=betamount,
                                         bet_type=bettype,
                                         bet_status='Proposed')

        else:
            bet = Bet()
            bet.game = gamestr
            bet.user1 = user1
            bet.bet_selection = bet_selection
            bet.bet_type = bettype
            bet.user2 = user2
            bet.bet_value = betamount
            # bet.bet_odds = bet_odds
            # bet.bet_payout = float(betamount) * ((bet_odds)/100.0)
            bet.bet_status = 'Proposed'
            bet.save()

            gamestr.bet_set.add(bet)


        if not user2.notifications.exists():
            bet_notice = user2.notifications.create(bet=bet,
                                                   sender=user1)

        else:
            bet_notice = Notification()
            bet_notice.bet = bet
            bet_notice.user = bet.user2
            bet_notice.sender = bet.user1
            bet_notice.save()

            user2.notifications.add(bet_notice)
