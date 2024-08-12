import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm

API_ENDPOINT = "http://192.168.200.23:8000/api/politician_register/"

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = {
                'politician_name': form.cleaned_data['username'],
                'politician_contact_number': form.cleaned_data['email'],
                'politician_password': form.cleaned_data['password'],
            }
            response = requests.post(API_ENDPOINT, data=data)

            if response.status_code == 201:  
                messages.success(request, 'Registration successful!')
            else:
                messages.error(request, 'Registration failed. Please try again.')

    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


# Login 

from .forms import LoginForm

API_LOGIN_ENDPOINT = "http://192.168.200.23:8000/api/politician_login/"

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = {
                'politician_name': form.cleaned_data['username'],
                'politician_password': form.cleaned_data['password'],
            }
            response = requests.post(API_LOGIN_ENDPOINT, data=data)

            if response.status_code == 200:  
                response_data = response.json()
                request.session['auth_token'] = response_data.get('token')  
                messages.success(request, 'Login successful!')
                return redirect('dashboard')                                  #  Redirect to the dashboard page
            else:
                messages.error(request, 'Login failed. Please check your username and password.')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


# Dashboard

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# @login_required
def dashboard(request):
    context = {
        'politician_name': request.user.username,
    }
    return render(request, 'dashboard.html', context)



def navbar(request):
    return render(request, 'navbar.html')


#  add town user list

def user_list(request):
    return render(request, 'users.html')

# add booth user list

def AddBoothUser(request):
    return render(request, 'AddBoothUser.html')

def BoothUser(request):
    return render(request, 'BoothUser.html')


def AddTownUser(request):
    return render(request, 'AddTownUser.html')


def ExitPoll(request):
    return render(request, 'ExitPoll.html')

def VotersList(request):
    return render(request, 'VotersList.html')

def KaryakartaList(request):
    return render(request, 'KaryakartaList.html')

def index(request):
    return render(request, 'index.html')

def TotalVoterList(request):
    return render(request, 'TotalVoterList.html')

def TownWiseVoterList(request):
    return render(request, 'TownWiseVoterList.html')

def CastWiseVoter(request):
    return render(request, 'CastWiseVoter.html')
