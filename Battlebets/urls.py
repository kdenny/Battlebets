from django.conf.urls import patterns, include, url
from django.contrib import admin
from bbapp import views



urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # url(r'^games/', views.games, name='games'),
    url(r'^bbapp/', include('bbapp.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^openid/(.*)', SessionConsumer()),
)