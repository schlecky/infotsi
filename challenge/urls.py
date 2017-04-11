from django.conf.urls import url
from . import views

app_name = 'challenge'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^epreuve/(?P<epreuve_id>[0-9]+)/resultat/$',
        views.ajouteCode, name='ajouteCode'),
    url(r'^epreuve/(?P<epreuve_id>[0-9]+)/$', views.editeCode, name='editeCode'),
    url(r'^login/$', views.loginView, name='loginView'),
    url(r'^accueil/$', views.accueilView, name='accueil'),
]
