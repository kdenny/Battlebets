from django.contrib import admin
from bbapp.models import UserProfile, Game, Bet, Notification

admin.site.register(UserProfile)
admin.site.register(Game)
admin.site.register(Bet)
admin.site.register(Notification)
