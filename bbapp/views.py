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

# Django REST Framework
from rest_framework import viewsets, mixins

# Scripts
from scripts.getOdds import getGames, addOddsToGame
from scripts.getScores import doScoresScrape, fixScores
from scripts.placeBet import makeBet

# Python
import simplejson as json
import requests
from pprint import pprint

from bbapp.models import *
from bbapp.forms import UserForm, UserProfileForm, BetForm



#################
# Index #
#################

def index(request):


    return render(request, 'bbapp/index.html')


def view_proposals(request):

    bet_proposals = Notification.objects.filter(user=request.user,bet__bet_status='Proposed')

    user_placed_bets = Notification.objects.filter(user=request.user,bet__user1=request.user,bet__bet_status='Accepted')

    user_accepted_bets = Notification.objects.filter(user=request.user,bet__user2=request.user,bet__bet_status='Accepted')

    declined_proposals = Notification.objects.filter(user=request.user,bet__user1=request.user,bet__bet_status='Declined',seen=False)

    gamedata = { "proposals" : bet_proposals, "user_placed" : user_placed_bets, "accepted" : user_accepted_bets, "declined" : declined_proposals}

    all_user_notifications = Notification.objects.filter(user=request.user)

    for un in all_user_notifications:
        un.seen = True
        un.save()

    resp =  render_to_response('bbapp/view_proposals.html', gamedata, context_instance=RequestContext(request))

    if request.method == 'POST':
        betstatus = request.POST.get('newstatus')
        betid = request.POST.get('betgame')
        print("")
        print("")
        print(betstatus)
        print(betid)

        q = Bet.objects.get(id=betid)
        q.bet_status = betstatus
        q.save()

        n = Notification.objects.get(user=request.user,bet__id=betid)
        n.seen = True
        n.save()

        other_user = q.user1

        if not other_user.notifications.exists():
            bet_notice = other_user.notifications.create(bet=q,
                                                   sender=request.user)

        else:
            bet_notice = Notification()
            bet_notice.bet = q
            bet_notice.user = other_user
            bet_notice.sender = request.user
            bet_notice.save()

            other_user.notifications.add(bet_notice)

        return resp






    return resp

#################
# Profile #
#################

def profile(request):


    return render(request, 'bbapp/profile.html')



#################
# Games List #
#################

# context_instance=Context(request)

def games_list(request):

    leagues = [
                'MLB',
                # 'PN-MLS',
                # 'WNBA'
               # 'PN_COPA_AMERICA',
               # 'PN-ME2016',
               ]

    for sport in leagues:
        info = {}
        info['league'] = sport

        ## Scrape scores from ESPN
        currentScores = doScoresScrape()
        fixScores(currentScores, sport)

        ## Get odds
        data = getGames(sport)
        addOddsToGame(data,sport)

        currentTime = datetime.now()
        currentHour = currentTime.hour
        currentDay = currentTime.day


        today = currentTime.strftime("%m/%d/%Y")

        if currentHour < 12:
            yesterday = datetime.now() - timedelta(days=1)
            print("Showing yesterday's games")
            today = yesterday.strftime("%m/%d/%Y")
        games = Game.objects.filter(date=today)
        gamedata = { "games" : games, "league" : info}

        resp =  render_to_response("bbapp/games_list.html", gamedata, context_instance=RequestContext(request))



    if request.method == 'POST':
        #### Place a bet
        madebet = False
        betselect = request.POST.get('betSelection')
        opponent = request.POST.get('users')
        betamount = request.POST.get('betval')
        user1 = request.user

        makeBet(betselect, opponent, betamount, user1)

        madebet = True




    return resp



#########################
# Snippet RESTful Model #
#########################



class CRUDBaseView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    pass

# class SnippetView(CRUDBaseView):
#     serializer_class = SnippetSerializer
#     queryset = Snippet.objects.all()


######################
# Registration Views #
######################

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)


        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user


            registered = True
            return HttpResponseRedirect('/bbapp/login/')
        else:
            print user_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()


    return render(request,
            'bbapp/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/bbapp/games_list/')
            else:
                return HttpResponse("Your Django Hackathon account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'bbapp/login.html', {})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/bbapp/login/')


