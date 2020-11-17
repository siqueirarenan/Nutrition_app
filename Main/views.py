from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.template import RequestContext
from Main.forms import SignUpForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password, ValidationError
from django.contrib.auth.forms import UserCreationForm
from django_ajax.decorators import ajax
from django.http import HttpResponseRedirect
from django.conf import settings
from .models import *
from django.contrib.auth.models import User


def homepage(request):
    context = {}
    return render(request, 'Main/homepage.html', context)

def dashboard(request):
    user_data = User.objects.get(username=request.user)
    user = UserGroup.objects.get(user=user_data)



    #people_group = user.group
    #days_in_action = datetime.today() - people_group.date_begin

    context = {'user_request': request.user,
               'user_data': user_data,
               'user_group': user,}
    return render(request, 'Main/dashboard.html', context)

def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/dashboard')
    else:
        form = SignUpForm()
    return render(request, 'registration/registration.html', {'form':form})


def signin(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                print(user)
                login(request, user)
                return redirect('/dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form':form})

def logout_view(request):
    logout(request)
    return render(request, 'Main/homepage.html', {})
