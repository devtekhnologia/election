
from django.urls import path
from .views import register, login, dashboard, user_list, AddTownUser, ExitPoll, VotersList, KaryakartaList, AddBoothUser, BoothUser, navbar, index, TotalVoterList
from .views import TownWiseVoterList
from .views import CastWiseVoter

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('', dashboard, name='dashboard'),
    path('users/', user_list, name='user_list'),
    path('exitpoll/', ExitPoll, name='ExitPoll'),
    path('add_booth_user/', AddBoothUser, name='AddBoothUser'),
    path('booth_user/', BoothUser, name='BoothUser'),
    path('town_user/', AddTownUser, name='AddTownUser'),
    path('VotersList/', VotersList, name='VotersList'),
    path('KaryakartaList/', KaryakartaList, name='KaryakartaList'),
    path('navbar/', navbar, name='navbar'),
    path('index/', index, name='index'),
    path('TotalVoterList/', TotalVoterList, name = 'TotalVoterList'),
    path('townwisevoterlist/', TownWiseVoterList, name = 'TownWiseVoterList'),
    path('castwisevoter/', CastWiseVoter, name = 'CastWiseVoter')

]
