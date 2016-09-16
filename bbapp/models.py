import uuid
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

import arrow


# Create your models here.
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # address = models.CharField(max_length=200, blank=True, default='')
    firstname = models.CharField(max_length=200, blank=True, default='')
    lastname = models.CharField(max_length=200, blank=True, default='')

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user

class Profile(models.Model):
    user = models.ForeignKey(User)

    def __unicode__(self):
        return unicode(self.user)


class Game(models.Model):
    # id = models.CharField(primary_key=True, max_length=10, blank=True, unique=True)
    gamekey = models.CharField(max_length=200, default='', unique=True, primary_key=True)
    league = models.CharField(max_length=5, default='')
    home_team = models.CharField(max_length=200, default='')
    home_odds = models.CharField(max_length=5, default='')
    home_short = models.CharField(max_length=5, default='')
    home_spread = models.CharField(max_length=5, default='')
    home_score = models.IntegerField(null=True)
    over_under = models.FloatField(null=True)
    away_team = models.CharField(max_length=200, default='')
    away_odds = models.CharField(max_length=5, default='')
    away_short = models.CharField(max_length=5, default='')
    away_spread = models.CharField(max_length=5, default='')
    away_score = models.IntegerField(null=True)
    status = models.CharField(max_length=20, default='')
    game_time = models.CharField(max_length=20, default='')
    date = models.CharField(max_length=200, default='')


    # def __init__(self, *args, **kwargs):
    #     super(Game, self).__init__(*args, **kwargs)
    #     self.id = str(uuid.uuid4())


    def __unicode__(self):
        # return unicode(self.id)
        # return u"Game ID {0} between {1} and {2}".format(self.id, self.home_team, self.away_team)
        return unicode(self.gamekey)

class Bet(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user1 = models.ForeignKey(User, related_name='user2')
    bet_selection = models.CharField(max_length=20, default='')
    user2 = models.ForeignKey(User, related_name='user1')
    bet_status = models.CharField(max_length=20, default='')
    bet_value = models.DecimalField(max_digits=6, decimal_places=2)
    # bet_odds = models.DecimalField(max_digits=6, decimal_places=2)
    # bet_payout = models.DecimalField(max_digits=6, decimal_places=2)
    created_date = models.DateTimeField('date created', default=datetime.now)
    changed_date = models.DateTimeField('date changed', default=datetime.now)
    bet_type = models.CharField(max_length=20, default='even')


    # def __init__(self, *args, **kwargs):
    #     super(Game, self).__init__(*args, **kwargs)
    #     self.id = str(uuid.uuid4())


    def __unicode__(self):
        # return unicode(self.id)
        return unicode(self.id)


class Notification(models.Model):
     user = models.ForeignKey(User, related_name="notifications")
     sender = models.ForeignKey(User, related_name="+")
     seen = models.BooleanField(default=False)
     bet = models.ForeignKey(Bet, on_delete=models.CASCADE)

     def __unicode__(self):
        return unicode(self.id)


# class BetProposal(Notification):
#
#      bet = models.ForeignKey(Bet, on_delete=models.CASCADE)
#      sentat = models.DateTimeField('date changed', default=datetime.now)
#
# class GameEnd(Notification):
#
#      bet = models.ForeignKey(Bet, on_delete=models.CASCADE)
#      winner = models.BooleanField(default=False)
#      endtime = models.DateTimeField('date changed', default=datetime.now)
#
# class FriendRequest(Notification):
#
#      senttime = models.DateTimeField('date changed', default=datetime.now)