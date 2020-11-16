from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from Main.forms import SignUpForm
from django.contrib.auth.password_validation import validate_password, ValidationError
from django.contrib.auth.forms import UserCreationForm
from django_ajax.decorators import ajax
from django.http import HttpResponseRedirect
from string import Template
import requests
from django.conf import settings


def homepage(request):
    context = {}
    return render(request, 'Main/home.html', context)

def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/registration.html', {'form':form})

