from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter
from django.views.generic import ListView

from bbapp import views
from bbapp.models import Game



router = DefaultRouter()
# router.register(r'snippets', views.SnippetView)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^index/$', views.index, name='index'),
    url(r'^games_list/', views.games_list, name='game_list'),
    url(r'^register/$', views.register, name='register'),
    url(r'^view_proposals/$', views.view_proposals, name='view_proposals'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    # url(r'^place_bet/(?P<game_id>\d+)/$', views.place_bet, name='place_bet'),

)
