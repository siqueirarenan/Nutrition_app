from datetime import datetime

from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.views import SignupView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.template import RequestContext
from Main.forms import SignUpForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.password_validation import validate_password, ValidationError
from django.contrib.auth.forms import UserCreationForm
from django_ajax.decorators import ajax
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from .models import *
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from Main.serializers import *


def homepage(request):
    context = {}
    return render(request, 'Main/homepage.html', context)

def dashboard(request):
    group = ""
    date_passed = ""
    user_data1 = User.objects.get(username=request.user)
    try:
        user_group = UserGroup.objects.get(user=user_data1)
        group = user_group.group
        date_passed = (datetime.today().date() - group.date_begin).days
        protocol = ProtocolMeal.objects.get(protocol=group.protocol)
    except:
        pass

    #Group tasks by line
    keys = []
    for task in TextTask.objects.all():
        keys += [task.position]
    for task in ChallengeTask.objects.all():
        keys += [task.position]
    grouped_tasks = {}
    for k in set(keys):
        grouped_tasks[k] = []
    for task in TextTask.objects.all():
        grouped_tasks[task.position] += [task]
    for task in ChallengeTask.objects.all():
        grouped_tasks[task.position] += [task]

    context = {'user_request': request.user,
               'user_data1': user_data1,
               'group': group,
               'date_passed': date_passed,
               'grouped_tasks': grouped_tasks.values()}
    return render(request, 'dashboard/dashboard.html', context)

def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/dashboard')
        else:
            #TODO: Fill form with inputed data
            return render(request, 'registration/registration.html', {'form':form})
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration.html', {'form':form})


def signin(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None :
                    login(request, user)
                    if user.is_active:
                        return redirect('/dashboard')
                    else:
                        return redirect('/accounts/inactive')
        else:
            return HttpResponse("Por favor, habilite cookies e tente novamente.")
    else:
        form = AuthenticationForm()
    request.session.set_test_cookie()
    return render(request, 'registration/login.html', {'form':form})

def password_change(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                return redirect('/password-change/done/')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'registration/passwordChangeForm.html', {'form': form})
    else:
        return redirect('/login')

def password_change_done(request):
    return render(request, 'registration/passwordChangeDone.html', {})

def logout_view(request):
    logout(request)
    return render(request, 'Main/homepage.html', {})

def signout(request):
    if request.user.is_authenticated:
        return render(request, 'registration/signout.html', {})
    else:
        return redirect('/login')

def signout_done(request):
    #request.user  is_active = False
    u = User.objects.get(username=request.user)
    u.is_active = False
    u.save()
    return render(request, 'registration/signout_done.html', {})




def recipes(request):
    recipe = Recipe.objects.all()
    context = {'recipes': recipe}
    return render(request, 'Main/recipes.html', context)


"""
TASKS
"""
def text_task(request,text_task_id):
    task = TextTask.objects.get(id=text_task_id)
    context = {'title': task.title,
               'text': task.text}
    return render(request, 'tasks/text.html', context)




"""
API endpoint that allows users to be viewed or edited.
"""
class UserViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('name')
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAdminUser]