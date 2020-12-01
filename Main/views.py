import copy
import json
from datetime import datetime
from itertools import chain
from smtplib import SMTPException
from string import Template

from allauth.socialaccount.models import SocialAccount
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework import permissions
from Main.serializers import *


def homepage(request,msg_sent_bool=0):
    context = {'msg_sent_bool': str(msg_sent_bool)}
    return render(request, 'Main/homepage.html', context)

def dashboard(request):
    group=""
    date_passed = ""
    user = ""
    completed_tasks = []
    social_user = None
    last_line_active = 0
    if request.user.is_authenticated:  #Otherwise, loads a case where everything is deactivated
        user = User.objects.get(username=request.user)
        try:
            social_user = SocialAccount.objects.get(user=user)
        except:
            pass
        try: #Otherwise, loads a case where everything is deactivated (when user has no group)
            user_group = UserGroup.objects.get(user=user)
            group = user_group.group
            if group.is_active:
                date_passed = (datetime.today().date() - group.date_begin).days
                completed_tasks = user_group.completed_tasks.all()
                last_line_active = group.last_task_line
        except:
            pass
    #Group tasks by line
    #ATENTION: the task classes here are treated in 2 different ways: by the task type class (sub), and the
    # general parent call AllTasks.
    #Unpacking list of lists. This makes a list of all tasks keeping the original subclasses of the tasks
    all_tasks_sub = [item for sublist in list(chain([list(chain(t.objects.all())) for t in AllTasks.__subclasses__()])) for item in sublist]
    keys = []
    for task in all_tasks_sub:
        if task.line_position > 0:
            keys += [task.line_position]
    grouped_tasks = {}
    for k in set(keys):
        if k <= last_line_active:
            grouped_tasks[k] = [[], ['auto']]   # [[arrays [task obj],[border color]], [if line links are active or not]]
        else:
            grouped_tasks[k] = [[], ['none']]   #Deactivate tasks lines that are not defined for the group
    for task_sub in all_tasks_sub:
        if task_sub.line_position > 0:
            grouped_tasks[task_sub.line_position][0] += [[]]
            grouped_tasks[task_sub.line_position][0][-1] += [task_sub]
            task_all_tasks = copy.copy(task_sub)
            task_all_tasks.__class__ = AllTasks
            grouped_tasks[task_sub.line_position][0][-1] += ['#33ff33' if task_all_tasks in completed_tasks else '#eeeeee']

    context = {'user_request': request.user,
               'user': user,
               'group': group,
               'date_passed': date_passed,
               'grouped_tasks_values': grouped_tasks.values(),
               'grouped_tasks_keys': grouped_tasks.keys(),
               'social_user': social_user
               }
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

def recipes(request,recip_open):
    recipes = Recipe.objects.all()
    favourite_recipes = None
    user_group = None
    if request.user.is_authenticated:  #Otherwise, loads a case where everything is deactivated
        user = User.objects.get(username=request.user)
        try: #Otherwise, loads a case where everything is deactivated (when user has no group)
            user_group = UserGroup.objects.get(user=user)
            if user_group.group.is_active:
                favourite_recipes = user_group.recipes.all()
        except:
            pass
    if request.method == 'POST':
        new_fav = Recipe.objects.get(name=list(request.POST.keys())[1])
        if list(request.POST.values())[1] == "1":
            user_group.recipes.add(new_fav)
        else:
            user_group.recipes.remove(new_fav)
        user_group.save()
        return HttpResponse(status=102)
    else:
        print(favourite_recipes)
        context = {'recipes': recipes,
                   'favourite_recipes': favourite_recipes,
                   'recip_open': recip_open,
                   'user_group': user_group
        }
        return render(request, 'dashboard/recipes.html', context)

def protocol(request,fg_open):
    user_group = ""
    favourite_food = ""
    protocol_meals = None
    if request.user.is_authenticated:  #Otherwise, loads a case where everything is deactivated
        user = User.objects.get(username=request.user)
        try: #Otherwise, loads a case where everything is deactivated (when user has no group)
            user_group = UserGroup.objects.get(user=user)
            people_group = user_group.group
            favourite_food = user_group.food.all()
            if people_group.is_active:
                group_protocol = people_group.protocol
                protocol_meals = ProtocolMeal.objects.filter(
                    protocol=group_protocol).order_by('meal_order')
        except:
            pass
    if request.method == 'POST':
        new_fav = FoodPortion.objects.get(name=list(request.POST.keys())[1])
        if list(request.POST.values())[1] == "1":
            user_group.food.add(new_fav)
            user_group.save()
        else:
            user_group.food.remove(new_fav)
            user_group.save()
        return HttpResponse(status=204)
    else:
        context = {'food_groups': FoodGroup.objects.all(),
                   'favourite_food': favourite_food,
                   'fg_open': fg_open,
                   'protocol_meals': protocol_meals
                   }
        return render(request, 'dashboard/protocol.html', context)

def favourites(request):
    favourite_recipes = None
    favourite_food = None
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        try:
            user_group = UserGroup.objects.get(user=user)
            if user_group.group.is_active:
                favourite_recipes = user_group.recipes.all()
                favourite_food = user_group.food.all()
        except:
            pass
    if request.method == 'POST':
        try:
            new_fav = Recipe.objects.get(name=list(request.POST.keys())[1])
            if list(request.POST.values())[1] == "1":
                user_group.recipes.add(new_fav)
            else:
                user_group.recipes.remove(new_fav)
        except:
            new_fav = FoodPortion.objects.get(name=list(request.POST.keys())[1])
            if list(request.POST.values())[1] == "1":
                user_group.food.add(new_fav)
            else:
                user_group.food.remove(new_fav)
        user_group.save()
        return HttpResponse(status=204)
    else:
        context = {'favourite_recipes': favourite_recipes,
                   'favourite_food': favourite_food,
                   }
        return render(request, 'dashboard/favourites.html', context)


def contact_submit(request):
    v_name = request.GET['Name']
    v_email = request.GET['Email']
    v_subject = request.GET['Subject']
    v_comment = request.GET['Comment']
    message_template = Template("APP CONTACT FORM\n\nName: ${NAME}\nEmail: ${EMAIL}\nSubject: ${SUBJECT}\n\nMessage:\n\n${MESSAGE}\n--")
    message = message_template.substitute(NAME=v_name,EMAIL=v_email,SUBJECT=v_subject,MESSAGE=v_comment)

    try:
        send_mail(
            v_name + " enviou uma menssagem",
            message,
            v_email,
            ['acessoria.marcelasiqueira@gmail.com'],
            fail_silently=False,
        )
        return HttpResponseRedirect("/1#contact")
    except SMTPException:
        return HttpResponseRedirect("/2#contact")


"""
TASKS
"""
def text_task(request,text_task_id):
    task = TextTask.objects.get(id=text_task_id)
    task_all = AllTasks.objects.get(id=text_task_id)
    user = User.objects.get(username=request.user)
    user_group = UserGroup.objects.get(user=user)
    is_complete = False
    if task_all in user_group.completed_tasks.all():
        is_complete = True
    elif request.method == 'POST':
        user_group.completed_tasks.add(task)
        is_complete = True
        user.save()
    context = {'task': task,
               'is_complete': is_complete }
    return render(request, 'tasks/text.html', context)

def challenge_task(request,challenge_task_id):
    task = ChallengeTask.objects.get(id=challenge_task_id)
    task_all = AllTasks.objects.get(id=challenge_task_id)
    user = User.objects.get(username=request.user)
    user_group = UserGroup.objects.get(user=user)
    is_complete = False
    if task_all in user_group.completed_tasks.all():
        is_complete = True
    elif request.method == 'POST':
        user_group.completed_tasks.add(task)
        is_complete = True
        user.save()

    context = {'task': task,
               'is_complete': is_complete }
    return render(request, 'tasks/challenge.html', context)

def multiple_choice_survey(request,multiple_choice_task_id):
    task = MultipleChoiceSurveyTask.objects.get(id=multiple_choice_task_id)
    task_all = AllTasks.objects.get(id=multiple_choice_task_id)
    choices = task.choices.splitlines()
    user = User.objects.get(username=request.user)
    user_group = UserGroup.objects.get(user=user)
    people_group = str(user_group.group)
    is_complete = False
    if task_all in user_group.completed_tasks.all():
        is_complete = True
    elif request.method == 'POST':
        i = 0
        for choice in choices:
            if choice in request.POST.values():
                SurveyVote(question=str(task),
                           people_group=people_group,
                           user=user,
                           choice=choices[i]).save()
            i += 1
        user_group.completed_tasks.add(task)
        is_complete = True
        user.save()
    context = {'task': task,
               'choices': choices,
               'is_complete': is_complete}
    return render(request, 'tasks/multiple_choice.html', context)

def writing_survey_task(request,writing_survey_id):
    task = WritingSurveyTask.objects.get(id=writing_survey_id)
    task_all = AllTasks.objects.get(id=writing_survey_id)
    user = User.objects.get(username=request.user)
    user_group = UserGroup.objects.get(user=user)
    people_group = str(user_group.group)
    is_complete = False
    if task_all in user_group.completed_tasks.all():
        is_complete = True
    elif request.method == 'POST':
        SurveyVote(question=str(task),
                   people_group=people_group,
                   user=user,
                   choice=request.POST['answer']).save()
        user_group.completed_tasks.add(task)
        is_complete = True
        user.save()
    context = {'task': task,
               'is_complete': is_complete}
    return render(request, 'tasks/writing_survey.html', context)

def calculation_task(request,calculation_task_id):
    task = CalculationTask.objects.get(id=calculation_task_id)
    result_sentence = task.result_sentence
    task_all = AllTasks.objects.get(id=calculation_task_id)
    fields = task.fields.splitlines()
    equations = task.equations.splitlines()
    user = User.objects.get(username=request.user)
    user_group = UserGroup.objects.get(user=user)
    calc_done = False
    if request.method == 'POST':
        values = list(request.POST.values())[1:]
        results = []
        for eq in equations:
            for f, v in zip(fields, values):  #first value is the csfr token
                eq = eq.replace(f, str(v))
            results += [eval(eq)]
        for r, i in zip(results, range(len(equations))):
            result_sentence = result_sentence.replace('eq' + str(i + 1), "%.1f" % r)
        calc_done = True
        if not task_all in user_group.completed_tasks.all():
            user_group.completed_tasks.add(task)
            user.save()
    context = {'title': task.title,
               'fields': fields,
               'result_sentence': result_sentence,
               'calc_done': calc_done}
    return render(request, 'tasks/calculation.html', context)

    # send_mail(
    #     'Subject here',
    #     'Here is the message.',
    #     'acessoria.marcelasiqueira@gmail.com',
    #     ['renansiqueira@gmail.com'],
    #     fail_silently=False,
    # )

def surveyresults(request, people_group):
    user = User.objects.get(username=request.user)
    if user.is_staff:
        if not people_group == "all":
            group_votes = SurveyVote.objects.filter(people_group=people_group)
        else:
            group_votes = SurveyVote.objects.all()
        surveys = MultipleChoiceSurveyTask.objects.all()
        results = {}
        for survey in surveys:
            question_votes = group_votes.filter(question=survey.question)
            #Count votes
            results[survey.question] = {}
            choices = survey.choices.splitlines()
            for c in choices:
                results[survey.question][str(c)] = 0
            for v in question_votes:
                results[survey.question][str(v.choice)] += 1
        surveys2 = WritingSurveyTask.objects.all()
        for survey in surveys2:
            question_votes = group_votes.filter(question=survey.question)
            results[survey.question] = []
            for a in question_votes:
                results[survey.question] += [a.choice]  #here 'choice' means the answer

        return HttpResponse(json.dumps(results, indent=4, sort_keys=True), content_type="application/json")
    else:
        return HttpResponse("Denied")


"""
API endpoint that allows users to be viewed or edited.
"""
# ViewSets define the view behavior.
class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAdminUser]

class SurveyVoteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SurveyVote.objects.all()
    serializer_class = SurveyVoteSerializer
    permission_classes = [permissions.IsAdminUser]

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]