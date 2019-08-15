from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns=[path('registracija/',views.registracija,name='registracija'),
             path('',views.registracija),
             path('login/',views.login_view,name='login'),
             path('kreiraj-clanak/', views.kreiraj_clanak, name='kreiraj-clanak'),
             path('odjava/', views.odjava, name='odjava'),
             url(r'^obrisi/(?P<slug>[\w-]+)/', views.obrisi_iz_korpice, name='obrisi'),
             path('blog/', views.prikazi_blog, name='blog'),
             url(r'blog/(?P<slug>[\w-]+)/', views.clanak_detalji, name='clanak'),
             path('korpica/', views.prikazi_korpicu, name='mojakorpica'),
             path('opis/(?P<slug>[\w-]*)/',views.opis,name='opis'),
             path('pretraga/', views.pretraga,name='prikazi'),path('pretraga/prikazi/', views.prikazi,name='prikaz'),
             url(r'^pretraga/prikazi/(?P<slug>[\w-]*)/provjera/', views.provjera),
             url(r'^pretraga/prikazi/(?P<slug>[\w-]*)/', views.dodaj_u_korpicu, name='card'),
             ]
