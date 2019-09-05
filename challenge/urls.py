from django.conf.urls import url
from . import views

app_name = 'challenge'
urlpatterns = [
    url(r'^$', views.accueilView, name='accueil'),
    url(r'^epreuve/(?P<epreuve_id>[0-9]+)/resultat/$',
        views.ajouteCode, name='ajouteCode'),
    url(r'^epreuve/(?P<epreuve_id>[0-9]+)/$', views.editeCode,
        name='editeCode'),
    url(r'^login/$', views.loginView, name='loginView'),
    url(r'^logout/$', views.logoutView, name='logoutView'),
    url(r'^accueil/$', views.accueilView, name='accueil'),
    url(r'^administration/$', views.administrationView, name='administration'),
    url(r'^notifications/$', views.notifView, name='notifications'),
    url(r'^administration/classements/$', views.classementView, name='classement'),
    url(r'^administration/verifieCodes/$', views.administrationView, name='administration'),
    url(r'^administration/statsEtudiant/(?P<etudiant_id>[0-9]+)/(?P<epreuve_id>[0-9]+)/$', views.adminStatsEtudiant, name='statistiques'),
    url(r'^administration/verifieCode/(?P<etudiant_id>[0-9]+)/(?P<epreuve_id>[0-9]+)/$', views.adminVerifieCode, name='verifieCode'),
]
