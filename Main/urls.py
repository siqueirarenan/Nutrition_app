from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


app_name = 'Main'
urlpatterns = [
    path('', views.homepage, name='homepage'),

    path('registration/', views.registration, name='registration'),
    path('login/', views.signin, name="login"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('logout/', views.logout_view, name='logged_out'),
    path('password-change/', views.password_change, name='password_change'),
    path('password-change/done/', views.password_change_done, name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name="registration/passwordResetForm.html",
        subject_template_name='registration/passwordResetSubject.txt',
        email_template_name = 'registration/passwordResetEmail.html'),
         name='password_reset'),
    #moved to main url.py because the app still uses the default email for reset, which doest have "Main:"
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('signout/', views.signout, name='signout'),
    path('signout/done', views.signout_done, name='signout_done'),


    path('dashboard/recipes/<str:recip_open>', views.recipes, name="recipes"),
    path('dashboard/protocol/<str:fg_open>', views.protocol, name="protocol"),
    path('dashboard/favourites', views.favourites, name="favourites"),


    #ADMIN
    path('surveyresults/<str:people_group>', views.surveyresults, name='surveyresults'),

    #TASKS
    path('task/text/<int:text_task_id>', views.text_task, name="text_task"),
    path('task/challenge/<int:challenge_task_id>', views.challenge_task, name="challenge_task"),
    path('task/multiple_choice_survey/<int:multiple_choice_task_id>',
         views.multiple_choice_survey, name="multiple_choice_survey_task"),
    path('task/writing_survey/<int:writing_survey_id>', views.writing_survey_task, name="writing_survey_task"),
    path('task/calculation/<int:calculation_task_id>', views.calculation_task, name="calculation_task"),


]

